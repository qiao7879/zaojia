from fastapi import APIRouter, Request, Path, Query, Depends
from fastapi.responses import Response
from typing import Annotated, Optional, Dict, Any
from common.dependency.db_dependency import DBSessionDependency
from common.dependency.pre_auth_dependency import PreAuthDependency
from common.dependency.current_user_dependency import CurrentUserDependency
from common.dependency.data_scope_dependency import DataScopeDependency
from common.dependency.role_auth_dependency import RoleAuthDependency  # 角色权限依赖
from common.model.response_model import ResponseUtil, ResponseBaseModel, DynamicResponseModel
from common.annotation.log_annotation import Log
from common.annotation.validate_fields_annotation import ValidateFields
from common.constant.business_type import BusinessType
from common.constant.role_constant import RoleConstant  # 角色常量

# 导入Service和VO
from modules.project.service.project_service import ProjectService
from modules.project.service.project_prefect_service import ProjectPrefectService
from modules.project.service.project_prefect_opinion_service import ProjectPrefectOpinionService
from modules.project.model.project_vo import AddProjectModel, EditProjectModel, ProjectDetailModel, ProjectPageModel
from modules.project.model.project_prefect_vo import UpdatePrefectStatusModel
from modules.project.model.project_do import SysProject  # 用于数据权限

# 路由配置（前缀：/system/project，分类：系统管理-项目管理）
project_controller = APIRouter(
    prefix='/system/project',
    tags=['系统管理-项目管理'],
    dependencies=[PreAuthDependency()]  # 全局登录认证
)

# ------------------------------ 项目主表接口 ------------------------------
# 1. 项目创建人新建项目
@project_controller.post(
    '',
    summary='项目创建人新建项目',
    description='仅项目创建人可新建项目，同步初始化流程',
    response_model=ResponseBaseModel,
    dependencies=[
        Depends(UserInterfaceAuthDependency('system:project:add')),
        Depends(RoleAuthDependency([RoleConstant.PROJECT_CREATOR]))  # 仅项目创建人
    ]
)
@ValidateFields(validate_model='add_project')
@Log(title='项目管理', business_type=BusinessType.INSERT)
async def add_project(
    request: Request,
    project: AddProjectModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[Dict[str, Any], CurrentUserDependency()]  # 当前用户信息（含角色）
) -> Response:
    result = await ProjectService.add_project_services(query_db, project, current_user)
    return ResponseUtil.success(msg=result.message, data=result.data)

# 2. 修改项目（已归档前可修改）
@project_controller.put(
    '/{project_id}',
    summary='修改项目',
    description='项目创建人、工程师、项目成员可修改，已归档不可修改',
    response_model=ResponseBaseModel,
    dependencies=[
        Depends(UserInterfaceAuthDependency('system:project:edit')),
        Depends(RoleAuthDependency([RoleConstant.PROJECT_CREATOR, RoleConstant.ENGINEER, RoleConstant.PROJECT_MEMBER]))
    ]
)
@ValidateFields(validate_model='edit_project')
@Log(title='项目管理', business_type=BusinessType.UPDATE)
async def edit_project(
    request: Request,
    project_id: Annotated[int, Path(description='项目ID')],
    project: EditProjectModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[Dict[str, Any], CurrentUserDependency()]
) -> Response:
    project.id = project_id  # 补充项目ID
    result = await ProjectService.edit_project_services(query_db, project, current_user)
    return ResponseUtil.success(msg=result.message)

# 3. 查询项目详情（含流程状态、历史意见）
@project_controller.get(
    '/{project_id}',
    summary='查询项目详情',
    description='查看项目基础信息、当前流程状态、是否显示开票用章按钮、历史审核意见',
    response_model=DynamicResponseModel[ProjectDetailModel],
    dependencies=[Depends(UserInterfaceAuthDependency('system:project:detail'))]
)
async def get_project_detail(
    request: Request,
    project_id: Annotated[int, Path(description='项目ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()]
) -> Response:
    detail_data = await ProjectService.get_project_detail_services(query_db, project_id)
    return ResponseUtil.success(model_content=detail_data)

# 4. 分页查询项目列表（按角色数据权限）
@project_controller.get(
    '/list',
    summary='分页查询项目列表',
    description='按角色数据权限过滤（如项目创建人看自己创建的项目）',
    response_model=DynamicResponseModel[ProjectPageModel],
    dependencies=[Depends(UserInterfaceAuthDependency('system:project:list'))]
)
async def get_project_page(
    request: Request,
    project_name: Annotated[Optional[str], Query(description='项目名称模糊查询')] = None,
    project_code: Annotated[Optional[str], Query(description='项目编号精确查询')] = None,
    page_num: Annotated[int, Query(description='当前页码')] = 1,
    page_size: Annotated[int, Query(description='每页条数')] = 10,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[Dict[str, Any], CurrentUserDependency()],
    data_scope_sql: Annotated[Any, DataScopeDependency(SysProject)]  # 角色数据权限SQL
) -> Response:
    query_params = {
        "project_name": project_name,
        "project_code": project_code,
        "page_num": page_num,
        "page_size": page_size
    }
    page_data = await ProjectService.get_project_page_services(query_db, query_params, data_scope_sql, current_user)
    return ResponseUtil.success(model_content=page_data)

# ------------------------------ 项目流程接口 ------------------------------
# 1. 项目创建人下发至工程师
@project_controller.put(
    '/prefect/send-engineer',
    summary='项目创建人下发至工程师',
    description='仅项目创建人可操作，同步记录下发意见',
    response_model=ResponseBaseModel,
    dependencies=[
        Depends(UserInterfaceAuthDependency('system:project:prefect:send')),
        Depends(RoleAuthDependency([RoleConstant.PROJECT_CREATOR]))
    ]
)
@ValidateFields(validate_model='update_prefect_status')
@Log(title='项目流程', business_type=BusinessType.UPDATE)
async def send_to_engineer(
    request: Request,
    prefect: UpdatePrefectStatusModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[Dict[str, Any], CurrentUserDependency()]
) -> Response:
    result = await ProjectPrefectService.creator_send_to_engineer_services(query_db, prefect, current_user)
    return ResponseUtil.success(msg=result.message)

# 2. 工程师提交至二级复审
@project_controller.put(
    '/prefect/engineer-submit',
    summary='工程师提交至二级复审',
    description='仅工程师可操作，同步记录修改意见',
    response_model=ResponseBaseModel,
    dependencies=[
        Depends(UserInterfaceAuthDependency('system:project:prefect:engineer-submit')),
        Depends(RoleAuthDependency([RoleConstant.ENGINEER]))
    ]
)
@ValidateFields(validate_model='update_prefect_status')
@Log(title='项目流程', business_type=BusinessType.UPDATE)
async def engineer_submit(
    request: Request,
    prefect: UpdatePrefectStatusModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[Dict[str, Any], CurrentUserDependency()]
) -> Response:
    result = await ProjectPrefectService.engineer_submit_review_services(query_db, prefect, current_user)
    return ResponseUtil.success(msg=result.message)

# 3. 二级复审操作（通过/驳回）
@project_controller.put(
    '/prefect/second-review',
    summary='二级复审操作',
    description='仅二级复核可操作，显示开票/用章按钮，同步记录复审意见',
    response_model=ResponseBaseModel,
    dependencies=[
        Depends(UserInterfaceAuthDependency('system:project:prefect:second-review')),
        Depends(RoleAuthDependency([RoleConstant.SECOND_REVIEWER]))
    ]
)
@ValidateFields(validate_model='update_prefect_status')
@Log(title='项目流程', business_type=BusinessType.UPDATE)
async def second_review(
    request: Request,
    prefect: UpdatePrefectStatusModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[Dict[str, Any], CurrentUserDependency()]
) -> Response:
    result = await ProjectPrefectService.second_review_services(query_db, prefect, current_user)
    return ResponseUtil.success(msg=result.message)

# 4. 三级复审操作（通过/驳回）
@project_controller.put(
    '/prefect/third-review',
    summary='三级复审操作',
    description='仅三级复核可操作，显示开票/用章按钮，同步记录复审意见',
    response_model=ResponseBaseModel,
    dependencies=[
        Depends(UserInterfaceAuthDependency('system:project:prefect:third-review')),
        Depends(RoleAuthDependency([RoleConstant.THIRD_REVIEWER]))
    ]
)
@ValidateFields(validate_model='update_prefect_status')
@Log(title='项目流程', business_type=BusinessType.UPDATE)
async def third_review(
    request: Request,
    prefect: UpdatePrefectStatusModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[Dict[str, Any], CurrentUserDependency()]
) -> Response:
    result = await ProjectPrefectService.third_review_services(query_db, prefect, current_user)
    return ResponseUtil.success(msg=result.message)

# 5. 归档人员查询待归档项目
@project_controller.get(
    '/prefect/to-archive',
    summary='查询待归档项目',
    description='仅归档人员可查看，分页展示待归档项目',
    response_model=ResponseBaseModel,
    dependencies=[
        Depends(UserInterfaceAuthDependency('system:project:prefect:to-archive')),
        Depends(RoleAuthDependency([RoleConstant.ARCHIVER]))
    ]
)
async def get_to_archive(
    request: Request,
    page_num: Annotated[int, Query(description='当前页码')] = 1,
    page_size: Annotated[int, Query(description='每页条数')] = 10,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[Dict[str, Any], CurrentUserDependency()]
) -> Response:
    to_archive_data = await ProjectPrefectService.get_to_archive_projects_services(query_db, page_num, page_size, current_user)
    return ResponseUtil.success(data=to_archive_data)

# 6. 归档人员执行归档
@project_controller.put(
    '/prefect/archive',
    summary='执行项目归档',
    description='仅归档人员可操作，流程结束，不可再修改',
    response_model=ResponseBaseModel,
    dependencies=[
        Depends(UserInterfaceAuthDependency('system:project:prefect:archive')),
        Depends(RoleAuthDependency([RoleConstant.ARCHIVER]))
    ]
)
@ValidateFields(validate_model='update_prefect_status')
@Log(title='项目流程', business_type=BusinessType.UPDATE)
async def archive_project(
    request: Request,
    prefect: UpdatePrefectStatusModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[Dict[str, Any], CurrentUserDependency()]
) -> Response:
    result = await ProjectPrefectService.archive_project_services(query_db, prefect, current_user)
    return ResponseUtil.success(msg=result.message)

# ------------------------------ 审核意见接口 ------------------------------
# 1. 查询项目所有历史意见
@project_controller.get(
    '/opinion/{project_id}',
    summary='查询项目历史审核意见',
    description='按时间倒序展示所有节点的审核意见',
    response_model=ResponseBaseModel,
    dependencies=[Depends(UserInterfaceAuthDependency('system:project:opinion:list'))]
)
async def get_project_opinions(
    request: Request,
    project_id: Annotated[int, Path(description='项目ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()]
) -> Response:
    opinion_list = await ProjectPrefectOpinionService.get_project_opinions_services(query_db, project_id)
    return ResponseUtil.success(data=opinion_list)


@project_controller.post(
    '/import',
    summary='Excel批量导入项目',
    description='仅项目创建人可操作，支持上传陈婷芳.xlsx格式文件，自动校验字段并批量导入',
    response_model=DynamicResponseModel[ProjectImportResponseModel],
    dependencies=[
        Depends(UserInterfaceAuthDependency('system:project:import')),
        Depends(RoleAuthDependency([RoleConstant.PROJECT_CREATOR]))  # 仅项目创建人
    ]
)
@Log(title='项目管理', business_type=BusinessType.IMPORT)  # 操作日志：导入类型
async def import_project_by_excel(
        request: Request,
        file: Annotated[UploadFile, File(description='陈婷芳.xlsx格式的项目文件')],
        query_db: Annotated[AsyncSession, DBSessionDependency()],
        current_user: Annotated[Dict[str, Any], CurrentUserDependency()]
) -> Response:
    # 1. 校验文件格式（仅允许.xlsx）
    if not file.filename.endswith('.xlsx'):
        return ResponseUtil.failure(msg='仅支持.xlsx格式的Excel文件，请上传陈婷芳.xlsx')

    # 2. 读取文件字节流
    try:
        file_bytes = await file.read()
        if not file_bytes:
            return ResponseUtil.failure(msg='上传的Excel文件为空')
    finally:
        await file.close()  # 确保文件关闭

    # 3. 调用Service层执行导入
    import_result = await ProjectService.import_project_by_excel_services(query_db, file_bytes, current_user)

    # 4. 返回导入结果
    return ResponseUtil.success(
        msg=f'Excel导入完成：成功{import_result.success_count}条，失败{import_result.fail_count}条',
        model_content=import_result
    )
