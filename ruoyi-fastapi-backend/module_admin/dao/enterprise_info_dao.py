from collections.abc import Sequence
from typing import Union

from sqlalchemy import delete, select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from module_admin.entity.do.enterprise_info_do import Enterprise
from module_admin.entity.do.role_do import SysRole, SysRoleMenu
from module_admin.entity.do.user_do import SysUser, SysUserRole
from module_admin.entity.vo.enterprise_info_vo import EnterpriseQueryModel, EnterpriseModel


class EnterpriseDao:
    """
    企业信息模块数据库操作层
    """

    @classmethod
    async def get_ent_detail_by_id(cls, db: AsyncSession, ent_id: int) -> Union[
        Enterprise, None]:
        """
        根据企业信息ID获取企业详细信息

        :param db: orm对象
        :param ent_id: 信息id
        :return: 菜单信息对象
        """
        # enterprise_info = (await db.execute(
        #     select(Enterprise).where(Enterprise.ent_id == enterprise_info))).scalars().first()
        enterprise_info = await db.get(Enterprise, ent_id)
        return enterprise_info

    @classmethod
    async def get_ent_detail_by_info(cls, db: AsyncSession, ent: EnterpriseModel) -> Union[
        Enterprise, None]:
        """
        根据企业信息ID获取企业详细信息

        :param db: orm对象
        :param ent: 信息id
        :return: 菜单信息对象
        """
        enterprise_info = (await db.execute(
            select(Enterprise).where(Enterprise.ent_id == ent.ent_id if ent.ent_id else True,
                                     Enterprise.enterprise_name == ent.enterprise_name if ent.enterprise_name else True,
                                     Enterprise.ent_type == ent.ent_type if ent.ent_type else True,
                                     Enterprise.bank_account == ent.bank_account if ent.bank_account else True,
                                     ))).scalars().first()

        return enterprise_info

    @classmethod
    async def get_ent_list(cls, db: AsyncSession, page_object: EnterpriseQueryModel) -> Sequence[
        Enterprise]:
        enterprise_info_list = (
            (
                await db.execute(
                    select(Enterprise)
                    .where(
                        Enterprise.enterprise_name.like(
                            f'%{page_object.enterprise_name}%') if page_object.enterprise_name else True,
                        Enterprise.contact_person.like(
                            f'%{page_object.contact_person}%') if page_object.contact_person else True,
                        Enterprise.contact_phone == page_object.contact_phone if page_object.contact_phone else True,
                        Enterprise.bank_account == page_object.bank_account if page_object.taxpayer_id else True
                    )
                    .order_by(Enterprise.create_time.desc())
                    .distinct()
                )
            )
            .scalars()
            .all()
        )
        return enterprise_info_list

    @classmethod
    async def add_ent_dao(cls, db: AsyncSession, enterprise_info: EnterpriseModel) -> Enterprise:
        """
        新增企业名称数据库操作

        :param db: orm对象
        :param enterprise_info: 菜单对象
        :return:
        """
        db_enterprise_info = Enterprise(**enterprise_info.model_dump())
        db.add(db_enterprise_info)
        await db.flush()

        return db_enterprise_info

    @classmethod
    async def edit_ent_dao(cls, db: AsyncSession, enterprise_info: dict) -> None:
        """
        编辑企业名称数据库操作

        :param db: orm对象
        :param enterprise_info: 需要更新的企业名称
        :return:
        """
        await db.execute(update(Enterprise), [enterprise_info])

    @classmethod
    async def delete_ent_dao(cls, db: AsyncSession, ent: EnterpriseModel) -> None:
        """
        删除企业名称数据库操作

        :param db: orm对象
        :param ent: 企业名称对象
        :return:
        """
        await db.execute(delete(Enterprise).where(Enterprise.ent_id.in_([ent.ent_id])))
