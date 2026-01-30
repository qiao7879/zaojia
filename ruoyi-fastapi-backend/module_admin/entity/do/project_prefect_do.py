from datetime import datetime

from sqlalchemy import CHAR, BigInteger, Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 1. 流程状态枚举（适配新流程：创建人→工程师→二级复审→三级复审→待归档→已归档）
PREFECT_STATUS_ENUM = {
    'CREATE': '01',  # 项目创建人新建（初始状态）
    'ENGINEER_EDIT': '02',  # 工程师修改中
    'SECOND_REVIEW': '03',  # 二级复审
    'THIRD_REVIEW': '04',  # 三级复审
    'TO_ARCHIVE': '05',  # 待归档（归档人员可见）
    'ARCHIVED': '06',  # 已归档（流程结束）
    'REJECT_ENGINEER': '12',  # 复审驳回至工程师（二级/三级复审均驳回至工程师）
}


# 2. 项目流程表（关联项目主表，记录流程状态）
class ProjectPrefect(Base):
    __tablename__ = 'project_prefect'
    __table_args__ = {'comment': '项目流程管理表', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_general_ci'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='流程ID')
    pro_id = Column(BigInteger, nullable=False, comment='关联项目ID（外键→sys_project.id）')
    current_status = Column(
        String(2),
        nullable=False,
        default=PREFECT_STATUS_ENUM['CREATE'],
        comment='当前流程状态（01-创建/02-工程师修改等）',
    )
    # 标记是否显示"开票/用章"按钮（二级/三级复审时为1，其他为0）
    show_invoice_seal = Column(CHAR(1), default='0', comment='是否显示开票/用章按钮（0-不显示/1-显示）')
    # 通用字段
    operator_id = Column(BigInteger, nullable=False, comment='操作人ID（外键→sys_user.id）')
    operator_name = Column(String(30), nullable=False, comment='操作人名称')
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    del_flag = Column(CHAR(1), default='0', comment='删除标志')
