from datetime import datetime
from typing import Annotated

from fastapi import Path, Query, Request
from fastapi.responses import Response
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession

from common.annotation.log_annotation import Log
from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.enums import BusinessType
from common.router import APIRouterPro
from common.vo import DataResponseModel, DynamicResponseModel, ResponseBaseModel
from module_admin.entity.vo.project_prefect_vo import BatchUpdatePrefectStatusModel, UpdatePrefectStatusModel
from module_admin.entity.vo.project_vo import (
    AddProjectModel,
    DeleteProjectModel,
    EditProjectModel,
    ProjectDetailModel,
    ProjectModel,
    ProjectPageModel,
)
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.project_prefect_opinion_service import ProjectPrefectOpinionService
from module_admin.service.project_prefect_service import ProjectPrefectService

# from module_admin.service.project_prefect_opinion_service import ProjectPrefectOpinionService
# from module_admin.service.project_prefect_service import ProjectPrefectService
from module_admin.service.project_service import ProjectService
from utils.log_util import logger
from utils.response_util import ResponseUtil

# 路由配置（前缀：/system/project，分类：系统管理-项目管理）
project_controller = APIRouterPro(
    prefix='/system/project',
    order_num=5,
    tags=['项目管理'],
    dependencies=[PreAuthDependency()],  # 全局登录认证
)


# ------------------------------ 项目主表接口 ------------------------------
# 1. 项目创建人新建项目
@project_controller.post(
    '',
    summary='项目创建人新建项目',
    description='仅项目创建人可新建项目，同步初始化流程',
    response_model=ResponseBaseModel,
    dependencies=[
        UserInterfaceAuthDependency('project:register:add'),
        # Depends(RoleAuthDependency([RoleConstant.PROJECT_CREATOR]))  # 仅项目创建人
    ],
)
@ValidateFields(validate_model='add_project')
@Log(title='项目管理', business_type=BusinessType.INSERT)
async def add_project(
    request: Request,
    project: AddProjectModel,
    # prefect_data: ProjectPrefectModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],  # 当前用户信息（含角色）
) -> Response:
    project.create_by = current_user.user.user_id
    project.create_name = current_user.user.nick_name
    project.create_time = datetime.now()
    project.update_by = current_user.user.user_id
    project.update_name = current_user.user.nick_name
    project.update_time = datetime.now()
    result = await ProjectService.add_project_services(query_db, project)
    logger.info(result.message)

    return ResponseUtil.success(msg=result.message)


# 2. 修改项目（已归档前可修改）
@project_controller.put(
    '',
    summary='编辑单位接口',
    description='用于编辑单位',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('project:register:update')],
)
@ValidateFields(validate_model='edit_project')
@Log(title='单位管理', business_type=BusinessType.UPDATE)
async def edit_projects(
    request: Request,
    edit_project: EditProjectModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_project.update_by = current_user.user.user_id
    edit_project.update_name = current_user.user.nick_name
    edit_project.update_time = datetime.now()
    # edit_project.status = 1
    edit_menu_result = await ProjectService.edit_project_services(query_db, edit_project)
    logger.info(edit_menu_result.message)

    return ResponseUtil.success(msg=edit_menu_result.message)


@project_controller.delete(
    '/{pro_ids}',
    summary='删除项目接口',
    description='用于删除项目',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('project:register:remove')],
)
@Log(title='项目管理', business_type=BusinessType.DELETE)
async def delete_system_projects(
    request: Request,
    pro_ids: Annotated[str, Path(description='需要删除的单位ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_menu = DeleteProjectModel(proIds=pro_ids)
    delete_menu_result = await ProjectService.delete_project_services(query_db, delete_menu)
    logger.info(delete_menu_result.message)

    return ResponseUtil.success(msg=delete_menu_result.message)


@project_controller.get(
    '/list',
    summary='获取单位列表接口',
    description='用于获取当前用户可见的单位列表',
    response_model=DataResponseModel[ProjectModel],
    dependencies=[UserInterfaceAuthDependency('project:register:list')],
)
async def get_system_menu_list(
    request: Request,
    project_query: Annotated[ProjectPageModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    menu_query_result = await ProjectService.get_project_list_services(query_db, project_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(data=menu_query_result)


# @project_controller.get(
#     '/{pro_id}',
#     summary='获取单位列表接口',
#     description='用于获取当前用户可见的单位列表',
#     response_model=DataResponseModel[ProjectModel],
#     dependencies=[UserInterfaceAuthDependency('project:ent:list')],
# )
# async def get_project_by_id(
#     request: Request,
#     pro_id: Annotated[int, Path(description='单位ID')],
#     query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
#     menu_query_result = await ProjectService.project_detail_services(query_db, pro_id)
#     logger.info('获取成功')
#
#     return ResponseUtil.success(data=menu_query_result)
#
# 3. 查询项目详情（含流程状态、历史意见）
@project_controller.get(
    '/{project_id}',
    summary='查询项目详情',
    description='查看项目基础信息、当前流程状态、是否显示开票用章按钮、历史审核意见',
    response_model=DynamicResponseModel[ProjectDetailModel],
    dependencies=[UserInterfaceAuthDependency('project:register:detail')],
)
async def get_project_detail(
    request: Request,
    project_id: Annotated[int, Path(description='项目ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    detail_data = await ProjectService.get_project_detail_services(query_db, project_id)
    logger.info('获取成功')

    return ResponseUtil.success(data=detail_data)


# ------------------------------ 项目流程接口 ------------------------------
# 1. 项目创建人下发至工程师
@project_controller.put(
    '/prefect/send-engineer',
    summary='项目创建人下发至工程师',
    description='仅项目创建人可操作，同步记录下发意见',
    response_model=ResponseBaseModel,
    dependencies=[
        UserInterfaceAuthDependency('project:prefect:send'),
        # Depends(RoleAuthDependency([RoleConstant.PROJECT_CREATOR]))
    ],
)
@ValidateFields(validate_model='update_prefect_status')
@Log(title='项目流程', business_type=BusinessType.UPDATE)
async def send_to_engineer(
    request: Request,
    prefect: UpdatePrefectStatusModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    prefect.operator_id = current_user.user.user_id
    prefect.operator_name = current_user.user.nick_name
    result = await ProjectPrefectService.creator_send_to_engineer_services(query_db, prefect, current_user)
    return ResponseUtil.success(msg=result.message)


#
# # 2. 工程师提交至二级复审
@project_controller.put(
    '/prefect/engineer-submit',
    summary='工程师提交至二级复审',
    description='仅工程师可操作，同步记录修改意见',
    response_model=ResponseBaseModel,
    dependencies=[
        UserInterfaceAuthDependency('project:prefect:engineer-submit'),
        # Depends(RoleAuthDependency([RoleConstant.ENGINEER]))
    ],
)
@ValidateFields(validate_model='update_prefect_status')
@Log(title='项目流程', business_type=BusinessType.UPDATE)
async def engineer_submit(
    request: Request,
    prefect: UpdatePrefectStatusModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    prefect.operator_id = current_user.user.user_id
    prefect.operator_name = current_user.user.nick_name
    result = await ProjectPrefectService.engineer_submit_review_services(query_db, prefect, current_user)
    return ResponseUtil.success(msg=result.message)


# 3. 二级复审操作（通过/驳回）
@project_controller.put(
    '/prefect/second-review',
    summary='二级复审操作',
    description='仅二级复核可操作，显示开票/用章按钮，同步记录复审意见',
    response_model=ResponseBaseModel,
    dependencies=[
        UserInterfaceAuthDependency('project:prefect:second-review'),
        # Depends(RoleAuthDependency([RoleConstant.SECOND_REVIEWER]))
    ],
)
@ValidateFields(validate_model='update_prefect_status')
@Log(title='项目流程', business_type=BusinessType.UPDATE)
async def second_review(
    request: Request,
    prefect: UpdatePrefectStatusModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    prefect.operator_id = current_user.user.user_id
    prefect.operator_name = current_user.user.nick_name
    result = await ProjectPrefectService.second_review_services(query_db, prefect, current_user)
    return ResponseUtil.success(msg=result.message)


# 4. 三级复审操作（通过/驳回）
@project_controller.put(
    '/prefect/third-review',
    summary='三级复审操作',
    description='仅三级复核可操作，显示开票/用章按钮，同步记录复审意见',
    response_model=ResponseBaseModel,
    dependencies=[
        UserInterfaceAuthDependency('project:prefect:third-review'),
        # Depends(RoleAuthDependency([RoleConstant.THIRD_REVIEWER]))
    ],
)
@ValidateFields(validate_model='update_prefect_status')
@Log(title='项目流程', business_type=BusinessType.UPDATE)
async def third_review(
    request: Request,
    prefect: UpdatePrefectStatusModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    prefect.operator_id = current_user.user.user_id
    prefect.operator_name = current_user.user.nick_name
    result = await ProjectPrefectService.third_review_services(query_db, prefect, current_user)
    return ResponseUtil.success(msg=result.message)


@project_controller.put(
    '/prefect/second-review/batch',
    summary='二级复审批量操作',
    description='仅二级复核可操作，同步记录复审意见',
    response_model=ResponseBaseModel,
    dependencies=[
        UserInterfaceAuthDependency('project:prefect:second-review'),
    ],
)
@Log(title='项目流程', business_type=BusinessType.UPDATE)
async def batch_second_review(
    request: Request,
    batch: BatchUpdatePrefectStatusModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await ProjectPrefectService.batch_second_review_services(query_db, batch, current_user)
    return ResponseUtil.success(msg=result.message)


@project_controller.put(
    '/prefect/third-review/batch',
    summary='三级复审批量操作',
    description='仅三级复核可操作，同步记录复审意见',
    response_model=ResponseBaseModel,
    dependencies=[
        UserInterfaceAuthDependency('project:prefect:third-review'),
    ],
)
@Log(title='项目流程', business_type=BusinessType.UPDATE)
async def batch_third_review(
    request: Request,
    batch: BatchUpdatePrefectStatusModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await ProjectPrefectService.batch_third_review_services(query_db, batch, current_user)
    return ResponseUtil.success(msg=result.message)


# 5. 归档人员查询待归档项目
@project_controller.get(
    '/prefect/to-archive',
    summary='查询待归档项目',
    description='仅归档人员可查看，分页展示待归档项目',
    response_model=ResponseBaseModel,
    dependencies=[
        UserInterfaceAuthDependency('system:project:prefect:to-archive'),
        # Depends(RoleAuthDependency([RoleConstant.ARCHIVER]))
    ],
)
async def get_to_archive(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
    page_num: Annotated[int, Query(description='当前页码')] = 1,
    page_size: Annotated[int, Query(description='每页条数')] = 10,
) -> Response:
    to_archive_data = await ProjectPrefectService.get_to_archive_projects_services(
        query_db, page_num, page_size, current_user
    )
    return ResponseUtil.success(data=to_archive_data)


# 6. 归档人员执行归档
@project_controller.put(
    '/prefect/archive',
    summary='执行项目归档',
    description='仅归档人员可操作，流程结束，不可再修改',
    response_model=ResponseBaseModel,
    dependencies=[
        UserInterfaceAuthDependency('system:project:prefect:archive'),
        # Depends(RoleAuthDependency([RoleConstant.ARCHIVER]))
    ],
)
@ValidateFields(validate_model='update_prefect_status')
@Log(title='项目流程', business_type=BusinessType.UPDATE)
async def archive_project(
    request: Request,
    prefect: UpdatePrefectStatusModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    prefect.operator_id = current_user.user.user_id
    prefect.operator_name = current_user.user.nick_name
    result = await ProjectPrefectService.archive_project_services(query_db, prefect, current_user)
    return ResponseUtil.success(msg=result.message)


# ------------------------------ 审核意见接口 ------------------------------
# 1. 查询项目所有历史意见
@project_controller.get(
    '/opinion/{project_id}',
    summary='查询项目历史审核意见',
    description='按时间倒序展示所有节点的审核意见',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('system:project:opinion:list')],
)
async def get_project_opinions(
    request: Request,
    project_id: Annotated[int, Path(description='项目ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    opinion_list = await ProjectPrefectOpinionService.get_project_opinions_services(query_db, project_id)
    return ResponseUtil.success(data=opinion_list)


# @project_controller.post(
#     '/import',
#     summary='Excel批量导入项目',
#     description='仅项目创建人可操作，支持上传陈婷芳.xlsx格式文件，自动校验字段并批量导入',
#     response_model=DynamicResponseModel[ProjectImportResponseModel],
#     dependencies=[
#         Depends(UserInterfaceAuthDependency('system:project:import')),
#         Depends(RoleAuthDependency([RoleConstant.PROJECT_CREATOR]))  # 仅项目创建人
#     ]
# )
# @Log(title='项目管理', business_type=BusinessType.IMPORT)  # 操作日志：导入类型
# async def import_project_by_excel(
#         request: Request,
#         file: Annotated[UploadFile, File(description='陈婷芳.xlsx格式的项目文件')],
#         query_db: Annotated[AsyncSession, DBSessionDependency()],
#         current_user: Annotated[Dict[str, Any], CurrentUserDependency()]
# ) -> Response:
#     # 1. 校验文件格式（仅允许.xlsx）
#     if not file.filename.endswith('.xlsx'):
#         return ResponseUtil.failure(msg='仅支持.xlsx格式的Excel文件，请上传陈婷芳.xlsx')
#
#     # 2. 读取文件字节流
#     try:
#         file_bytes = await file.read()
#         if not file_bytes:
#             return ResponseUtil.failure(msg='上传的Excel文件为空')
#     finally:
#         await file.close()  # 确保文件关闭
#
#     # 3. 调用Service层执行导入
#     import_result = await ProjectService.import_project_by_excel_services(query_db, file_bytes, current_user)
#
#     # 4. 返回导入结果
#     return ResponseUtil.success(
#         msg=f'Excel导入完成：成功{import_result.success_count}条，失败{import_result.fail_count}条',
#         model_content=import_result
#     )
