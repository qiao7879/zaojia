from datetime import datetime
from sqlalchemy import Column, BigInteger, String, DECIMAL, CHAR, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from utils.common_util import SqlalchemyUtil

Base = declarative_base()


# 项目主表（字段基于陈婷芳.xlsx提取，含基础信息、业务数据）
class SysProject(Base):
    __tablename__ = 'sys_project'
    __table_args__ = {
        'comment': '项目主表',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci'
    }

    # 基础字段
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='项目ID（主键）')
    project_code = Column(String(30), nullable=False, unique=True, comment='项目编号（唯一，如XM20260101）')
    project_name = Column(String(100), nullable=False, comment='项目名称（Excel核心字段）')
    project_type = Column(String(20), nullable=True, comment='项目类型（如研发项目/运维项目，Excel字段）')
    dept_id = Column(BigInteger, nullable=False, comment='所属部门ID（外键→sys_dept.id）')
    dept_name = Column(String(50), nullable=False, comment='所属部门名称')

    # 业务字段（基于Excel提取，示例）
    project_manager = Column(String(30), nullable=False, comment='项目经理（Excel字段）')
    start_date = Column(DateTime, nullable=False, comment='项目开始时间（Excel字段）')
    end_date = Column(DateTime, nullable=True, comment='项目预计结束时间（Excel字段）')
    project_budget = Column(DECIMAL(18, 2), nullable=True, comment='项目预算（Excel字段）')
    project_desc = Column(Text, nullable=True, comment='项目描述（Excel字段）')
    status = Column(CHAR(1), default='0', comment='项目状态（0-正常/1-暂停/2-终止）')

    # 通用字段（软删除、创建/更新信息）
    create_by = Column(BigInteger, nullable=False, comment='创建人ID（外键→sys_user.id，项目创建人）')
    create_name = Column(String(30), nullable=False, comment='创建人名称')
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    update_by = Column(BigInteger, nullable=True, comment='更新人ID')
    update_name = Column(String(30), nullable=True, comment='更新人名称')
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    del_flag = Column(CHAR(1), default='0', comment='删除标志（0-存在/2-删除）')
