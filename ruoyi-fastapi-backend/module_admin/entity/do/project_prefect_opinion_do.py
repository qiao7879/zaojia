from datetime import datetime

from sqlalchemy import CHAR, BigInteger, Column, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 项目流程意见表（独立存储各节点审核意见，支持回溯）
class ProjectPrefectOpinion(Base):
    __tablename__ = 'project_prefect_opinion'
    __table_args__ = {
        'comment': '项目流程审核意见表',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
    }

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='意见ID')
    project_id = Column(BigInteger, nullable=False, comment='关联项目ID')
    prefect_id = Column(BigInteger, nullable=False, comment='关联流程ID（外键→sys_project_prefect.id）')
    node_code = Column(String(2), nullable=False, comment='意见对应的流程节点（01-创建/02-工程师修改/03-二级复审等）')
    node_name = Column(String(255), nullable=False, comment='对应的流程节点名称')
    opinion_content = Column(Text, nullable=True, comment='审核意见/修改说明（核心字段）')
    # 操作人信息
    operator_id = Column(BigInteger, nullable=False, comment='填写意见人ID')
    operator_name = Column(String(30), nullable=False, comment='填写意见人名称')
    operator_role = Column(String(30), nullable=False, comment='填写意见人角色（如二级复核/工程师）')
    # 时间信息
    create_time = Column(DateTime, default=datetime.now, comment='意见填写时间')
    del_flag = Column(CHAR(1), default='0', comment='删除标志')
