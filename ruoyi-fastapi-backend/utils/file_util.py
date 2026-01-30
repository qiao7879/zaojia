# app/common/utils/file_util.py
import os
from datetime import datetime

import aiofiles
from fastapi import UploadFile

from config.env import UploadConfig
from utils.upload_util import UploadUtil  # 导入框架自带工具类


class FileUtil:
    """通用文件工具类（整合框架UploadUtil）"""

    @staticmethod
    def generate_unique_filename(original_filename: str) -> str:
        """
        生成唯一文件名（基于框架UploadUtil扩展）
        格式：原始名_时间戳_机器码_随机码.后缀
        示例：陈婷芳_20260120153020_M123.xlsx
        """
        # 提取原始文件名和后缀
        name_part, ext_part = os.path.splitext(original_filename)
        ext_part = ext_part.lower()
        # 生成时间戳（框架工具类校验格式）
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        # 框架自带随机码（3位）
        random_code = UploadUtil.generate_random_number()
        # 拼接唯一文件名（兼容框架校验规则）
        unique_name = f'{name_part}_{timestamp}{UploadConfig.UPLOAD_MACHINE}{random_code}{ext_part}'
        return unique_name

    @staticmethod
    def validate_file(file: UploadFile) -> tuple[bool, str]:
        """
        校验文件（整合框架UploadUtil的校验规则）
        :param file: FastAPI UploadFile对象
        :return: (是否通过, 错误信息)
        """
        # 1. 框架自带：校验文件后缀
        if not UploadUtil.check_file_extension(file):
            return False, f'文件类型不允许，仅支持：{",".join(UploadConfig.DEFAULT_ALLOWED_EXTENSION)}'

        # 2. 校验文件大小（字节转MB）
        file_size_mb = file.size / 1024 / 1024
        # 按文件类型匹配大小限制
        ext = file.filename.rsplit('.', 1)[-1].lower()
        if ext in ['xlsx', 'xls']:
            size_limit = UploadConfig.FILE_SIZE_LIMIT['EXCEL']
        elif ext in ['jpg', 'jpeg', 'png', 'gif']:
            size_limit = UploadConfig.FILE_SIZE_LIMIT['IMAGE']
        elif ext in ['pdf', 'doc', 'docx']:
            size_limit = UploadConfig.FILE_SIZE_LIMIT['DOCUMENT']
        else:
            size_limit = UploadConfig.FILE_SIZE_LIMIT['DEFAULT']

        if file_size_mb > size_limit:
            return False, f'文件大小超过限制（最大{size_limit}MB），当前：{file_size_mb:.2f}MB'

        # 3. 若文件名是已生成的唯一名称，校验时间戳/机器码/随机码（框架规则）
        if UploadConfig.UPLOAD_MACHINE in file.filename:
            if not UploadUtil.check_file_timestamp(file.filename):
                return False, '文件时间戳格式不合法（需为YYYYMMDDHHMMSS）'
            if not UploadUtil.check_file_machine(file.filename):
                return False, f'文件机器码不合法（需为{UploadConfig.UPLOAD_MACHINE}）'
            if not UploadUtil.check_file_random_code(file.filename):
                return False, '文件随机码不合法（需为3位数字）'

        return True, ''

    @staticmethod
    def get_file_storage_path(business_type: str, file_alias: str) -> str:
        """
        获取文件存储完整路径（基于框架配置）
        :param business_type: 业务类型
        :param file_alias: 唯一文件名
        :return: 完整路径
        """
        # 按业务类型分目录（基于框架根路径）
        business_path = os.path.join(UploadConfig.UPLOAD_ROOT_PATH, business_type)
        # 确保目录存在
        if not os.path.exists(business_path):
            os.makedirs(business_path, exist_ok=True)
        # 完整路径
        return os.path.join(business_path, file_alias)

    @staticmethod
    def generate_file_url(file_alias: str, business_type: str) -> str:
        """
        生成文件访问URL（基于框架配置）
        """
        return f'{UploadConfig.FILE_ACCESS_PREFIX}{business_type}/{file_alias}'

    @staticmethod
    async def save_file_async(file: UploadFile, storage_path: str) -> None:
        """
        异步保存文件（复用框架UploadUtil的异步逻辑）
        :param file: UploadFile对象
        :param storage_path: 存储路径
        """
        # 检查文件是否已存在（框架工具类）
        if UploadUtil.check_file_exists(storage_path):
            raise FileExistsError(f'文件{storage_path}已存在')

        # 异步写入文件（框架风格）
        async with aiofiles.open(storage_path, 'wb') as f:
            while chunk := await file.read(1024 * 1024):  # 按1MB分片读取
                await f.write(chunk)

    @staticmethod
    async def generate_file_async(filepath: str) -> UploadUtil.generate_file:
        """
        异步生成文件二进制流（直接复用框架工具类）
        """
        async for chunk in UploadUtil.generate_file(filepath):
            yield chunk
