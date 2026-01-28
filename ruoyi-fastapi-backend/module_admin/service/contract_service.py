from typing import Any, Union

from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_admin.dao.contract_dao import ContractDao
from module_admin.entity.vo.contract_vo import ContractModel, ContractPageQueryModel, DeleteContractModel
from utils.common_util import CamelCaseUtil


class ContractService:
    """
    合同管理模块服务层
    """

    @classmethod
    async def get_contract_list_services(
        cls, query_db: AsyncSession, page_object: ContractPageQueryModel, is_page: bool = False
    ) -> Union[PageModel, list[dict[str, Any]]]:
        """
        获取合同分页列表service
        """

        contract_list_result = await ContractDao.get_contract_list(query_db, page_object, is_page=is_page)
        return contract_list_result

    @classmethod
    async def add_contract_services(cls, query_db: AsyncSession, page_object: ContractModel) -> CrudResponseModel:
        """
        新增合同service
        """

        try:
            contract_info = ContractModel(**page_object.model_dump(by_alias=True))
            await ContractDao.add_contract_dao(query_db, contract_info)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_contract_services(cls, query_db: AsyncSession, page_object: ContractModel) -> CrudResponseModel:
        """
        编辑合同service
        """

        if not page_object.contract_id:
            raise ServiceException(message='合同ID不能为空')

        contract_info = await cls.contract_detail_services(query_db, page_object.contract_id)
        if not contract_info.contract_id:
            raise ServiceException(message='合同不存在')

        try:
            edit_contract = page_object.model_dump(exclude_unset=True)
            await ContractDao.edit_contract_dao(query_db, edit_contract)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='更新成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def delete_contract_services(
        cls, query_db: AsyncSession, page_object: DeleteContractModel
    ) -> CrudResponseModel:
        """
        删除合同service
        """

        if not page_object.contract_ids:
            raise ServiceException(message='传入合同id为空')

        contract_id_list = page_object.contract_ids.split(',')
        try:
            for contract_id in contract_id_list:
                contract_id = contract_id.strip()
                if not contract_id:
                    continue
                await ContractDao.delete_contract_dao(query_db, ContractModel(contractId=int(contract_id)))
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='删除成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def contract_detail_services(cls, query_db: AsyncSession, contract_id: int) -> ContractModel:
        """
        获取合同详情service
        """

        contract = await ContractDao.get_contract_detail_by_id(query_db, contract_id)
        result = ContractModel(**CamelCaseUtil.transform_result(contract)) if contract else ContractModel()
        return result
