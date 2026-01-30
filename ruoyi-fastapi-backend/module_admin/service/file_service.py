import os
from datetime import datetime
from typing import Any

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.exception import ServiceException
from module_admin.dao.file_dao import FileDao
from module_admin.entity.vo.file_vo import BatchFileUploadResponseModel, FileUploadModel, FileUploadResponseModel

# from app.modules.common.file.model.file_vo import (
#     FileUploadModel, FileUploadResponseModel, BatchFileUploadResponseModel
# )
from utils.file_util import FileUtil  # 导入整合后的工具类
from utils.upload_util import UploadUtil

# from app.common.exception.service_exception import ServiceException


class FileService:
    """通用文件Service层（整合框架UploadUtil）"""

    # 1. 单文件上传（核心方法）
    @classmethod
    async def upload_file_services(
        cls, db: AsyncSession, file: UploadFile, upload_model: FileUploadModel, current_user: dict[str, Any]
    ) -> FileUploadResponseModel:
        """
        通用单文件上传（基于框架UploadUtil）
        """
        # 1.1 基础校验
        if not file or not file.filename:
            raise ServiceException(message='上传文件不能为空')

        # 1.2 框架规则：校验文件（后缀/大小/命名规则）
        is_valid, error_msg = FileUtil.validate_file(file)
        if not is_valid:
            raise ServiceException(message=error_msg)

        # 1.3 生成唯一文件名（兼容框架命名规则）
        file_alias = FileUtil.generate_unique_filename(file.filename)
        # 1.4 获取存储路径（基于框架配置）
        storage_path = FileUtil.get_file_storage_path(upload_model.business_type, file_alias)

        # 1.5 异步保存文件（复用框架UploadUtil的异步逻辑）
        try:
            await FileUtil.save_file_async(file, storage_path)
        except FileExistsError as e:
            raise ServiceException(message=f'文件保存失败：{e!s}') from e
        except Exception as e:
            raise ServiceException(message=f'文件保存失败：{e!s}') from e
        finally:
            await file.close()

        # 1.6 构造文件信息（入库）
        file_info = {
            'file_name': file.filename,
            'file_alias': file_alias,
            'file_type': file.filename.rsplit('.', 1)[-1].lower(),
            'file_size': file.size,
            'file_path': storage_path,
            'file_url': FileUtil.generate_file_url(file_alias, upload_model.business_type),
            'upload_user_id': current_user['user_id'],
            'upload_user_name': current_user['user_name'],
            'business_type': upload_model.business_type,
            'business_id': upload_model.business_id or '',
            'status': '0',
        }

        # 1.7 保存到数据库
        db_file = await FileDao.add_file_dao(db, file_info)
        await db.commit()

        # 1.8 返回结果
        return FileUploadResponseModel(
            file_id=db_file.id,
            file_name=file.filename,
            file_alias=file_alias,
            file_url=file_info['file_url'],
            file_size=file.size,
            upload_time=db_file.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        )

    # 2. 批量文件上传（适配框架工具类）
    @classmethod
    async def batch_upload_file_services(
        cls, db: AsyncSession, files: list[UploadFile], upload_model: FileUploadModel, current_user: dict[str, Any]
    ) -> BatchFileUploadResponseModel:
        success_count = 0
        fail_count = 0
        file_list = []
        fail_details = []

        for idx, file in enumerate(files):
            try:
                if not file or not file.filename:
                    fail_count += 1
                    fail_details.append(f'第{idx + 1}个文件：文件为空')
                    continue

                # 框架规则：校验文件
                is_valid, error_msg = FileUtil.validate_file(file)
                if not is_valid:
                    fail_count += 1
                    fail_details.append(f'第{idx + 1}个文件（{file.filename}）：{error_msg}')
                    continue

                # 生成唯一文件名
                file_alias = FileUtil.generate_unique_filename(file.filename)
                storage_path = FileUtil.get_file_storage_path(upload_model.business_type, file_alias)

                # 异步保存文件
                await FileUtil.save_file_async(file, storage_path)
                await file.close()

                # 构造文件记录
                file_info = {
                    'file_name': file.filename,
                    'file_alias': file_alias,
                    'file_type': file.filename.rsplit('.', 1)[-1].lower(),
                    'file_size': file.size,
                    'file_path': storage_path,
                    'file_url': FileUtil.generate_file_url(file_alias, upload_model.business_type),
                    'upload_user_id': current_user['user_id'],
                    'upload_user_name': current_user['user_name'],
                    'business_type': upload_model.business_type,
                    'business_id': upload_model.business_id or '',
                    'status': '0',
                }
                file_list.append(file_info)
                success_count += 1

            except Exception as e:
                fail_count += 1
                fail_details.append(f'第{idx + 1}个文件（{file.filename if file else "未知"}）：{e!s}')
                if file:
                    await file.close()
                continue

        # 批量入库
        if file_list:
            await FileDao.batch_add_file_dao(db, file_list)
            await db.commit()

        # 构造返回结果
        file_response_list = [
            FileUploadResponseModel(
                file_name=info['file_name'],
                file_alias=info['file_alias'],
                file_url=info['file_url'],
                file_size=info['file_size'],
                upload_time=datetime.fromtimestamp(os.path.getctime(info['file_path'])).strftime('%Y-%m-%d %H:%M:%S'),
            )
            for info in file_list
        ]

        return BatchFileUploadResponseModel(
            success_count=success_count, fail_count=fail_count, file_list=file_response_list, fail_details=fail_details
        )

    # 3. 文件下载（复用框架异步生成文件逻辑）
    @classmethod
    async def download_file_services(cls, db: AsyncSession, file_id: int) -> dict[str, Any]:
        # 查询文件记录
        db_file = await FileDao.get_file_by_id(db, file_id)
        if not db_file:
            raise ServiceException(message='文件不存在或已被删除')

        # 框架工具类：检查文件是否存在
        if not UploadUtil.check_file_exists(db_file.file_path):
            raise ServiceException(message='文件已被删除（本地存储不存在）')

        # 返回文件信息（包含异步生成器）
        return {
            'file_path': db_file.file_path,
            'file_name': db_file.file_name,
            'file_type': db_file.file_type,
            'file_generator': FileUtil.generate_file_async(db_file.file_path),  # 框架异步生成器
        }
