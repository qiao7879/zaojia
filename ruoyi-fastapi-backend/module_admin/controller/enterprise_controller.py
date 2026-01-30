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
from common.vo import DataResponseModel, ResponseBaseModel
from module_admin.entity.vo.enterprise_info_vo import (
    DeleteEnterpriseModel,
    EnterpriseModel,
    EnterprisePageModel,
)
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.enterprise_service import EnterpriseService
from utils.log_util import logger
from utils.response_util import ResponseUtil

menu_controller = APIRouterPro(
    prefix='/project/ent', order_num=5, tags=['项目管理-单位管理'], dependencies=[PreAuthDependency()]
)


@menu_controller.get(
    '/list',
    summary='获取单位列表接口',
    description='用于获取当前用户可见的单位列表',
    response_model=DataResponseModel[list[EnterpriseModel]],
    dependencies=[UserInterfaceAuthDependency('project:ent:list')],
)
async def get_system_menu_list(
    request: Request,
    menu_query: Annotated[EnterprisePageModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    menu_query_result = await EnterpriseService.get_ent_list_services(query_db, menu_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(data=menu_query_result)


@menu_controller.post(
    '',
    summary='新增单位接口',
    description='用于新增单位',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('project:ent:add')],
)
@ValidateFields(validate_model='add_ent')
@Log(title='单位管理', business_type=BusinessType.INSERT)
async def add_system_menu(
    request: Request,
    add_ent: EnterpriseModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_ent.create_by = current_user.user.user_name
    add_ent.create_time = datetime.now()
    add_ent.update_by = current_user.user.user_name
    add_ent.update_time = datetime.now()
    add_menu_result = await EnterpriseService.add_ent_services(query_db, add_ent)
    logger.info(add_menu_result.message)

    return ResponseUtil.success(msg=add_menu_result.message)


@menu_controller.put(
    '',
    summary='编辑单位接口',
    description='用于编辑单位',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('project:ent:edit')],
)
@ValidateFields(validate_model='edit_menu')
@Log(title='单位管理', business_type=BusinessType.UPDATE)
async def edit_system_menu(
    request: Request,
    edit_menu: EnterpriseModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_menu.update_by = current_user.user.user_name
    edit_menu.update_time = datetime.now()
    edit_menu_result = await EnterpriseService.edit_ent_services(query_db, edit_menu)
    logger.info(edit_menu_result.message)

    return ResponseUtil.success(msg=edit_menu_result.message)


@menu_controller.delete(
    '/{ent_ids}',
    summary='删除单位接口',
    description='用于删除单位',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('project:ent:remove')],
)
@Log(title='单位管理', business_type=BusinessType.DELETE)
async def delete_system_menu(
    request: Request,
    ent_ids: Annotated[str, Path(description='需要删除的单位ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_menu = DeleteEnterpriseModel(entIds=ent_ids)
    delete_menu_result = await EnterpriseService.delete_ent_services(query_db, delete_menu)
    logger.info(delete_menu_result.message)

    return ResponseUtil.success(msg=delete_menu_result.message)


@menu_controller.get(
    '/{ent_id}',
    summary='获取单位详情接口',
    description='用于获取指定单位的详情信息',
    response_model=DataResponseModel[EnterpriseModel],
    dependencies=[UserInterfaceAuthDependency('project:ent:query')],
)
async def query_detail_system_menu(
    request: Request,
    ent_id: Annotated[int, Path(description='单位ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    menu_detail_result = await EnterpriseService.ent_detail_services(query_db, ent_id)
    logger.info(f'获取menu_id为{ent_id}的信息成功')

    return ResponseUtil.success(data=menu_detail_result)
