from typing import Any, Union

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_admin.entity.do.contract_do import Contract
from module_admin.entity.vo.contract_vo import ContractModel, ContractPageQueryModel
from utils.page_util import PageUtil


class ContractDao:
    """
    合同管理模块数据库操作层
    """

    @classmethod
    async def get_contract_detail_by_id(cls, db: AsyncSession, contract_id: int) -> Union[Contract, None]:
        """
        根据合同ID获取合同详情
        """

        contract = await db.get(Contract, contract_id)
        return contract

    @classmethod
    async def get_contract_list(
        cls, db: AsyncSession, page_object: ContractPageQueryModel, is_page: bool = True
    ) -> Union[PageModel, list[dict[str, Any]]]:
        """
        获取合同分页列表
        """

        query = (
            select(Contract)
            .where(
                Contract.contract_name.like(f'%{page_object.contract_name}%') if page_object.contract_name else True,
                Contract.contract_type == page_object.contract_type if page_object.contract_type else True,
            )
            .order_by(Contract.create_time.desc())
            .distinct()
        )
        contract_list: Union[PageModel, list[dict[str, Any]]] = await PageUtil.paginate(
            db, query, page_object.page_num, page_object.page_size, is_page
        )
        return contract_list

    @classmethod
    async def add_contract_dao(cls, db: AsyncSession, contract_info: ContractModel) -> Contract:
        """
        新增合同数据库操作
        """

        db_contract = Contract(**contract_info.model_dump())
        db.add(db_contract)
        await db.flush()
        return db_contract

    @classmethod
    async def edit_contract_dao(cls, db: AsyncSession, contract_info: dict) -> None:
        """
        编辑合同数据库操作
        """

        await db.execute(update(Contract), [contract_info])

    @classmethod
    async def delete_contract_dao(cls, db: AsyncSession, contract: ContractModel) -> None:
        """
        删除合同数据库操作
        """

        await db.execute(delete(Contract).where(Contract.contract_id.in_([contract.contract_id])))
