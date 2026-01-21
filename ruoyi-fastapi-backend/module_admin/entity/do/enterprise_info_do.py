from sqlalchemy import Column, BigInteger, String, DateTime, UniqueConstraint, Index
from datetime import datetime

from sqlalchemy import CHAR, BigInteger, Column, DateTime, Integer, SmallInteger, String


from config.database import Base






class Enterprise(Base):
    """
    企业单位信息表
    """

    __tablename__ = 'enterprise_info'
    __table_args__ = (
        # 唯一约束：纳税人识别号
        UniqueConstraint('taxpayer_id', name='uk_taxpayer_id'),
        # 普通索引：企业名称
        Index('idx_enterprise_name', 'enterprise_name'),
        {'comment': '企业基本信息表'}
    )

    ent_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='主键ID')
    enterprise_name = Column(String(200), nullable=False, comment='企业名称')
    taxpayer_id = Column(String(20), nullable=False, comment='纳税人识别号')
    ent_type = Column(
        BigInteger,
        nullable=False,
        server_default="1",
        comment='企业类型'
    )
    address = Column(
        String(500),
        nullable=True,
        # 复用你原有代码中的空值默认值设置方式
        server_default=None,  # 若需要适配多数据库，可替换为下面注释的代码
        comment='企业地址'
    )
    contact_person = Column(
        String(50),
        nullable=True,
        server_default=None,
        comment='联系人'
    )
    contact_phone = Column(
        String(20),
        nullable=True,
        server_default=None,
        comment='联系电话'
    )
    bank_name = Column(
        String(100),
        nullable=True,
        server_default=None,
        comment='开户行'
    )
    bank_account = Column(
        String(30),
        nullable=True,
        server_default=None,
        comment='银行账号'
    )
    create_by = Column(String(64), nullable=False, comment='创建人ID（外键→sys_user.id，项目创建人）')
    create_name = Column(String(30), nullable=False, comment='创建人名称')
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    update_by = Column(String(64), nullable=True, comment='更新人ID')
    update_name = Column(String(30), nullable=True, comment='更新人名称')
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
