# app/modules/common/file/controller/file_controller.py
from fastapi import APIRouter, Request, Depends, File, UploadFile, Path, Query
from fastapi.responses import Response, StreamingResponse
from typing import Annotated, List, Dict, Any, Optional
# from app.common.dependency.db_dependency import DBSessionDependency
# from app.common.dependency.pre_auth_dependency import PreAuthDependency
# from app.common.dependency.current_user_dependency import CurrentUserDependency
# from app.common.model.response_model import ResponseUtil, DynamicResponseModel
# from app.common.annotation.log_annotation import Log
# from app.common.constant.business_type import BusinessType
#
# # 导入Service和VO
# from app.modules.common.file.service.file_service import FileService
# from app.modules.common.file.model.file_vo import (
#     FileUploadModel, FileUploadResponseModel, BatchFileUploadResponseModel, FileQueryModel
# )
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.pre_auth import PreAuthDependency
from common.enums import BusinessType
from common.vo import DynamicResponseModel
from module_admin.entity.vo.file_vo import FileUploadResponseModel

# 公共文件路由
file_controller = APIRouter(
    prefix='/api/v1/common/file',
    tags=['公共模块-文件管理'],
    dependencies=[PreAuthDependency()]
)


# ------------------------------
# 1. 单文件上传（整合框架UploadUtil）
# ------------------------------
@file_controller.post(
    '/upload',
    summary='通用单文件上传',
    description='基于框架UploadUtil实现，支持文件后缀/大小/命名规则校验',
    response_model=DynamicResponseModel[FileUploadResponseModel]
)
@Log(title='文件管理', business_type=BusinessType.UPLOAD)
async def upload_file(
        request: Request,
        file: Annotated[UploadFile, File(description='待上传的文件')],
        business_type: Annotated[str, Query(description='业务类型（如project_import/contract_attach）')],
        business_id: Annotated[Optional[str], Query(description='关联业务ID')] = None,
        query_db: Annotated[AsyncSession, DBSessionDependency()],
        current_user: Annotated[Dict[str, Any], CurrentUserDependency()]
) -> Response:
    upload_model = FileUploadModel(business_type=business_type, business_id=business_id)
    upload_result = await FileService.upload_file_services(query_db, file, upload_model, current_user)
    return ResponseUtil.success(msg='文件上传成功', model_content=upload_result)


# ------------------------------
# 2. 批量文件上传
# ------------------------------
@file_controller.post(
    '/batch/upload',
    summary='通用批量文件上传',
    response_model=DynamicResponseModel[BatchFileUploadResponseModel]
)
@Log(title='文件管理', business_type=BusinessType.UPLOAD)
async def batch_upload_file(
        request: Request,
        files: Annotated[List[UploadFile], File(description='待上传的文件列表')],
        business_type: Annotated[str, Query(description='业务类型')],
        business_id: Annotated[Optional[str], Query(description='关联业务ID')] = None,
        query_db: Annotated[AsyncSession, DBSessionDependency()],
        current_user: Annotated[Dict[str, Any], CurrentUserDependency()]
) -> Response:
    upload_model = FileUploadModel(business_type=business_type, business_id=business_id)
    upload_result = await FileService.batch_upload_file_services(query_db, files, upload_model, current_user)
    return ResponseUtil.success(
        msg=f'批量上传完成：成功{upload_result.success_count}个，失败{upload_result.fail_count}个',
        model_content=upload_result
    )


# ------------------------------
# 3. 文件下载（复用框架异步生成器）
# ------------------------------
@file_controller.get(
    '/download/{file_id}',
    summary='通用文件下载'
)
@Log(title='文件管理', business_type=BusinessType.DOWNLOAD)
async def download_file(
        request: Request,
        file_id: Annotated[int, Path(description='文件ID')],
        query_db: Annotated[AsyncSession, DBSessionDependency()]
) -> StreamingResponse:
    # 获取文件信息（包含异步生成器）
    file_info = await FileService.download_file_services(query_db, file_id)

    # 使用框架异步生成器返回流式响应
    return StreamingResponse(
        file_info["file_generator"],
        media_type=f'application/{file_info["file_type"]}',
        headers={
            "Content-Disposition": f'attachment; filename="{file_info["file_name"]}"'
        }
    )


# ------------------------------
# 4. 查询文件列表
# ------------------------------
@file_controller.get(
    '/list',
    summary='查询文件列表'
)
async def get_file_list(
        request: Request,
        business_type: Annotated[str, Query(description='业务类型')],
        business_id: Annotated[str, Query(description='关联业务ID')],
        page_num: Annotated[int, Query(description='页码')] = 1,
        page_size: Annotated[int, Query(description='每页条数')] = 10,
        query_db: Annotated[AsyncSession, DBSessionDependency()]
) -> Response:
    query_model = FileQueryModel(
        business_type=business_type,
        business_id=business_id,
        page_num=page_num,
        page_size=page_size
    )
    file_page = await FileDao.get_file_page_dao(db=query_db, query_params=query_model)
    return ResponseUtil.success(data=file_page)
