from datetime import datetime

from sqlalchemy import CHAR, FLOAT, Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

# 声明基类（根据你的项目实际导入方式调整）
Base = declarative_base()


class Project(Base):
    __tablename__ = 'project'
    __table_args__ = {'comment': '项目主表', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_general_ci'}

    # 基础字段（保留示例中的核心基础字段）
    pro_id = Column(Integer, primary_key=True, autoincrement=True, comment='项目ID（主键）')
    project_code = Column(String(50), nullable=True, unique=True, comment='项目唯一编码（如XM20260101）')
    project_name = Column(String(255), nullable=True, comment='项目全称（Excel核心字段）')
    project_type = Column(String(20), nullable=True, comment='项目类型（如研发项目/运维项目，Excel字段）')

    # 业务核心字段（基于提供的数据库字段定义）
    ent_id = Column(Integer, nullable=True, comment='项目所属企业ID（外键→enterprise_info.ent_id）')
    ent_name = Column(String(200), nullable=True, comment='项目业主单位名称')
    service_content = Column(String(100), nullable=True, comment='项目服务内容')
    user_company = Column(String(100), nullable=True, comment='项目使用单位')
    project_manager = Column(String(50), nullable=True, comment='我方项目负责人（Excel字段）')
    coordinator = Column(String(100), nullable=True, comment='项目配合人员')
    contract_signed = Column(String(20), nullable=True, comment='合同签订状态')
    document_obtained = Column(String(20), nullable=True, comment='是否已取得相关文件')
    contract_amount = Column(FLOAT, nullable=True, default=0.00, comment='项目合同金额（元）')
    contract_discount = Column(String(50), nullable=True, comment='合同折扣说明')
    deliverable_completed = Column(String(20), nullable=True, comment='项目成果完成状态')
    control_price_review = Column(String(50), nullable=True, comment='控制价或控制价评审金额')
    settlement_submitted = Column(FLOAT, nullable=True, default=0.00, comment='结算送审金额（元）')
    settlement_approved = Column(FLOAT, nullable=True, default=0.00, comment='结算审定金额（元）')
    invoice_should_amount = Column(FLOAT, nullable=True, comment='项目应开具发票金额（元）')
    payment_applied = Column(String(20), nullable=True, comment='是否已申请付款')
    payment_month = Column(String(20), nullable=True, comment='请款月份')
    invoice_issued = Column(String(20), nullable=True, comment='是否已开具发票')
    invoice_date = Column(DateTime, nullable=True, comment='发票开具日期')
    invoice_issued_amount = Column(FLOAT, nullable=True, comment='已开具发票金额（元）')
    invoice_remaining_amount = Column(FLOAT, nullable=True, comment='剩余可开具发票金额（元）')
    payment_received = Column(String(20), nullable=True, comment='业主是否已回款')
    payment_received_amount = Column(FLOAT, nullable=True, comment='已回款金额（元）')
    payment_received_date = Column(DateTime, nullable=True, comment='回款到账日期')
    payment_remaining_amount = Column(FLOAT, nullable=True, default=0.00, comment='剩余未回款金额（元）')
    payment_recovery_rate = Column(FLOAT, nullable=True, default=0.00, comment='项目回款率')
    reconciliation_done = Column(String(20), nullable=True, comment='是否已与业主对账')
    reconciliation_date = Column(DateTime, nullable=True, comment='双方对账日期')
    reconciliation_voucher = Column(String(255), nullable=True, comment='对账凭证说明或编号')
    commission_accrued = Column(String(20), nullable=True, comment='是否已计提提成')
    commission_amount = Column(FLOAT, nullable=True, default=0.00, comment='提成金额（元）')
    commission_date = Column(DateTime, nullable=True, comment='提成计提日期')
    contract_electronic_saved = Column(String(20), nullable=True, comment='合同电子档是否已存档')
    contract_file = Column(String(255), nullable=True, comment='合同文件编号')
    deliverable_electronic_saved = Column(String(20), nullable=True, comment='成果文件电子档是否已存档')
    deliverable_file = Column(String(255), nullable=True, comment='成果文件编号')
    document_paper_saved = Column(String(20), nullable=True, comment='纸质资料存档情况')
    document_save_type = Column(String(100), nullable=True, comment='资料存档类型说明')
    remarks = Column(String(500), nullable=True, comment='项目其他备注信息')

    # 项目时间相关字段（示例中的字段）
    start_date = Column(DateTime, nullable=True, comment='项目开始时间（Excel字段）')
    end_date = Column(DateTime, nullable=True, comment='项目预计结束时间（Excel字段）')
    project_budget = Column(FLOAT, nullable=True, comment='项目预算（Excel字段）')
    project_desc = Column(Text, nullable=True, comment='项目描述（Excel字段）')
    status = Column(CHAR(1), default='0', comment='项目状态（0-正常/1-暂停/2-终止）')
    prefect_status = Column(String(255), default='01', comment='项目流程状态（01-创建/02-工程师修改等）')

    # 通用字段（软删除、创建/更新信息）
    create_by = Column(Integer, nullable=True, comment='创建人ID（外键→sys_user.id，项目创建人）')
    create_name = Column(String(30), nullable=True, comment='创建人名称')
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    update_by = Column(Integer, nullable=True, comment='更新人ID')
    update_name = Column(String(30), nullable=True, comment='更新人名称')
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    del_flag = Column(CHAR(1), default='0', comment='删除标志（0-存在/2-删除）')
