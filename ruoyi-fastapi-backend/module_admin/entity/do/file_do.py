# app/modules/common/file/model/file_do.py
from datetime import datetime

from sqlalchemy import CHAR, BigInteger, Column, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 文件存储状态枚举
FILE_STATUS_ENUM = {
    'NORMAL': '0',  # 正常
    'DELETE': '1',  # 已删除（软删除）
}


# 通用文件存储表
class SysFile(Base):
    __tablename__ = 'sys_file'
    __table_args__ = {'comment': '通用文件存储表', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_general_ci'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='文件ID（主键）')
    file_name = Column(String(255), nullable=False, comment='原始文件名（如陈婷芳.xlsx）')
    file_alias = Column(
        String(255), nullable=False, unique=True, comment='存储别名（唯一，如20260120_1030_abc123.xlsx）'
    )
    file_type = Column(String(50), nullable=False, comment='文件类型（如xlsx/png/pdf）')
    file_size = Column(BigInteger, nullable=False, comment='文件大小（字节）')
    file_path = Column(Text, nullable=False, comment='文件存储路径（绝对路径/OSS路径）')
    file_url = Column(Text, nullable=True, comment='文件访问URL（前端下载/预览用）')
    upload_user_id = Column(BigInteger, nullable=False, comment='上传人ID（外键→sys_user.id）')
    upload_user_name = Column(String(30), nullable=False, comment='上传人名称')
    business_type = Column(String(50), nullable=False, comment='业务类型（如project_import/contract_attach）')
    business_id = Column(String(64), nullable=True, comment='关联业务ID（如项目ID/合同ID）')
    status = Column(CHAR(1), default=FILE_STATUS_ENUM['NORMAL'], comment='文件状态（0-正常/1-删除）')
    create_time = Column(DateTime, default=datetime.now, comment='上传时间')
    del_flag = Column(CHAR(1), default='0', comment='软删除标志（0-存在/2-删除）')
