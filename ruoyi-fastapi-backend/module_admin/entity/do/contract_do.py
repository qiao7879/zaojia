from datetime import datetime

from sqlalchemy import DECIMAL, Column, Date, DateTime, Integer, String

from config.database import Base


class Contract(Base):
    """
    合同表
    """

    __tablename__ = 'contract'
    __table_args__ = {'comment': '合同表'}

    contract_id = Column(Integer, primary_key=True, autoincrement=True, comment='合同ID')
    contract_name = Column(String(255), nullable=True, comment='合同名称')
    contract_type = Column(String(255), nullable=True, comment='合同类型')
    contract_amount = Column(DECIMAL(10, 2), nullable=True, comment='合同金额')
    contract_status = Column(String(255), nullable=True, comment='合同状态')
    contract_sign_date = Column(Date, nullable=True, comment='合同签署日期')
    contract_effective_date = Column(Date, nullable=True, comment='合同生效日期')
    contract_expire_date = Column(Date, nullable=True, comment='合同过期日期')
    contract_terminate_date = Column(Date, nullable=True, comment='合同终止日期')
    contract_operator = Column(String(255), nullable=True, comment='合同操作人')
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    create_by = Column(String(255), nullable=True, comment='创建人')
    update_time = Column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    update_by = Column(String(255), nullable=True, comment='更新人')
