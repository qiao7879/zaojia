from datetime import datetime
from typing import Annotated

from fastapi import Path, Query, Request, Response
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession

from common.annotation.log_annotation import Log
from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.enums import BusinessType
from common.router import APIRouterPro
from common.vo import DataResponseModel, PageResponseModel, ResponseBaseModel
from module_admin.entity.vo.contract_vo import ContractModel, ContractPageQueryModel, DeleteContractModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.contract_service import ContractService
from utils.log_util import logger
from utils.response_util import ResponseUtil

contract_controller = APIRouterPro(
    prefix='/project/contract', order_num=6, tags=['项目管理-合同管理'], dependencies=[PreAuthDependency()]
)


@contract_controller.get(
    '/list',
    summary='获取合同分页列表接口',
    description='用于获取合同分页列表',
    response_model=PageResponseModel[ContractModel],
    dependencies=[UserInterfaceAuthDependency('project:contract:list')],
)
async def get_contract_list(
    request: Request,
    contract_page_query: Annotated[ContractPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    contract_page_query_result = await ContractService.get_contract_list_services(
        query_db, contract_page_query, is_page=True
    )
    logger.info('获取成功')
    return ResponseUtil.success(model_content=contract_page_query_result)


@contract_controller.post(
    '',
    summary='新增合同接口',
    description='用于新增合同',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('project:contract:add')],
)
@ValidateFields(validate_model='add_contract')
@Log(title='合同管理', business_type=BusinessType.INSERT)
async def add_contract(
    request: Request,
    add_contract: ContractModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_contract.create_by = current_user.user.user_name
    add_contract.create_time = datetime.now()
    add_contract.update_by = current_user.user.user_name
    add_contract.update_time = datetime.now()
    add_contract_result = await ContractService.add_contract_services(query_db, add_contract)
    logger.info(add_contract_result.message)
    return ResponseUtil.success(msg=add_contract_result.message)


@contract_controller.put(
    '',
    summary='编辑合同接口',
    description='用于编辑合同',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('project:contract:edit')],
)
@ValidateFields(validate_model='edit_contract')
@Log(title='合同管理', business_type=BusinessType.UPDATE)
async def edit_contract(
    request: Request,
    edit_contract: ContractModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_contract.update_by = current_user.user.user_name
    edit_contract.update_time = datetime.now()
    edit_contract_result = await ContractService.edit_contract_services(query_db, edit_contract)
    logger.info(edit_contract_result.message)
    return ResponseUtil.success(msg=edit_contract_result.message)


@contract_controller.delete(
    '/{contract_ids}',
    summary='删除合同接口',
    description='用于删除合同',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('project:contract:remove')],
)
@Log(title='合同管理', business_type=BusinessType.DELETE)
async def delete_contract(
    request: Request,
    contract_ids: Annotated[str, Path(description='需要删除的合同ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_contract_model = DeleteContractModel(contractIds=contract_ids)
    delete_contract_result = await ContractService.delete_contract_services(query_db, delete_contract_model)
    logger.info(delete_contract_result.message)
    return ResponseUtil.success(msg=delete_contract_result.message)


@contract_controller.get(
    '/{contract_id}',
    summary='获取合同详情接口',
    description='用于获取指定合同的详情信息',
    response_model=DataResponseModel[ContractModel],
    dependencies=[UserInterfaceAuthDependency('project:contract:query')],
)
async def query_contract_detail(
    request: Request,
    contract_id: Annotated[int, Path(description='合同ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    contract_detail_result = await ContractService.contract_detail_services(query_db, contract_id)
    logger.info(f'获取contract_id为{contract_id}的信息成功')
    return ResponseUtil.success(data=contract_detail_result.model_dump(by_alias=True))
