from typing import Any, Union

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_admin.entity.do.enterprise_info_do import Enterprise
from module_admin.entity.vo.enterprise_info_vo import EnterpriseModel, EnterprisePageModel
from utils.page_util import PageUtil


class EnterpriseDao:
    """
    企业信息模块数据库操作层
    """

    @classmethod
    async def get_ent_detail_by_id(cls, db: AsyncSession, ent_id: int) -> Union[Enterprise, None]:
        """
        根据企业信息ID获取企业详细信息

        :param db: orm对象
        :param ent_id: 信息id
        :return: 菜单信息对象
        """
        enterprise_info = await db.get(Enterprise, ent_id)
        return enterprise_info

    @classmethod
    async def get_ent_detail_by_info(cls, db: AsyncSession, ent: EnterpriseModel) -> Union[Enterprise, None]:
        """
        根据企业信息ID获取企业详细信息

        :param db: orm对象
        :param ent: 信息id
        :return: 菜单信息对象
        """
        enterprise_info = (
            (
                await db.execute(
                    select(Enterprise).where(
                        Enterprise.ent_id == ent.ent_id if ent.ent_id else True,
                        Enterprise.enterprise_name == ent.enterprise_name if ent.enterprise_name else True,
                        Enterprise.ent_type == ent.ent_type if ent.ent_type else True,
                        Enterprise.bank_account == ent.bank_account if ent.bank_account else True,
                    )
                )
            )
            .scalars()
            .first()
        )

        return enterprise_info

    @classmethod
    async def get_ent_list(
        cls, db: AsyncSession, page_object: EnterprisePageModel, is_page: bool = True
    ) -> Union[PageModel, list[dict[str, Any]]]:
        enterprise_info_list = (
            select(Enterprise)
            .where(
                Enterprise.enterprise_name.like(f'%{page_object.enterprise_name}%')
                if page_object.enterprise_name
                else True,
                Enterprise.contact_person.like(f'%{page_object.contact_person}%')
                if page_object.contact_person
                else True,
                Enterprise.contact_phone == page_object.contact_phone if page_object.contact_phone else True,
                Enterprise.ent_type == page_object.ent_type if page_object.ent_type else True,
                Enterprise.bank_account == page_object.bank_account if page_object.taxpayer_id else True,
            )
            .order_by(Enterprise.create_time.desc())
            .distinct()
        )
        post_list: Union[PageModel, list[dict[str, Any]]] = await PageUtil.paginate(
            db, enterprise_info_list, page_object.page_num, page_object.page_size, is_page
        )
        return post_list

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
