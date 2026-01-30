from collections.abc import Sequence
from typing import Any, Union

from sqlalchemy import Row, RowMapping, and_, delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_admin.entity.do.menu_do import SysMenu
from module_admin.entity.do.project_do import Project
from module_admin.entity.do.project_prefect_do import ProjectPrefect
from module_admin.entity.do.role_do import SysRole
from module_admin.entity.do.user_do import SysUser, SysUserRole
from module_admin.entity.vo.project_vo import (
    ProjectModel,
    ProjectPageModel,
)
from utils.common_util import CamelCaseUtil


class ProjectDao:
    """项目主表数据访问层"""

    @classmethod
    async def get_project_list_dao(
        cls, db: AsyncSession, page_object: ProjectPageModel, role: list ,user_id: int, is_page: bool = True
    ) -> Union[PageModel, list[dict[str, Any]]]:
        """
        根据查询参数获取项目列表信息
        :param db: orm对象
        :param page_object: 查询参数对象
        :param user_id: 查询参数对象
        :param role: 查询参数对象
        :param is_page: 是否分页查询
        :return: 项目列表信息对象
        """
        if is_page:
            if role in ['admin', 'a_admin']:
                pass
            elif role in []:
                pass



    @classmethod
    async def get_project_list(
        cls, db: AsyncSession, page_object: ProjectPageModel, is_page: bool = False
    ) -> Union[PageModel, list[dict[str, Any]]]:
        """
        根据查询参数获取岗位列表信息

        :param db: orm对象
        :param page_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 岗位列表信息对象
        """

        status_list: list[str] = []
        if page_object.prefect_status:
            if isinstance(page_object.prefect_status, str) and ',' in page_object.prefect_status:
                status_list = [s.strip() for s in page_object.prefect_status.split(',') if s.strip()]
            else:
                status_list = [page_object.prefect_status]

        query = (
            select(
                Project,
                ProjectPrefect.current_status.label('review_status'),
                ProjectPrefect.operator_name.label('reviewer'),
                ProjectPrefect.update_time.label('review_time'),
            )
            .outerjoin(
                ProjectPrefect,
                and_(
                    ProjectPrefect.pro_id == Project.pro_id,
                    ProjectPrefect.del_flag == '0',
                ),
            )
            .where(
                Project.del_flag == '0',
                Project.project_name.like(f'%{page_object.project_name}%') if page_object.project_name else True,
                Project.project_code.like(f'%{page_object.project_code}%') if page_object.project_code else True,
                Project.project_type.like(f'%{page_object.project_type}%') if page_object.project_type else True,
                Project.prefect_status.in_(status_list) if status_list else True,
                Project.payment_received == page_object.payment_received if page_object.payment_received else True,
            )
            .order_by(Project.create_time.desc())
            .distinct()
        )

        if is_page:
            total = (await db.execute(select(func.count('*')).select_from(query.subquery()))).scalar() or 0
            query_result = await db.execute(
                query.offset((page_object.page_num - 1) * page_object.page_size).limit(page_object.page_size)
            )
            rows: list[dict[str, Any]] = []
            for row in query_result:
                project_obj = row[0]
                project_dict = ProjectModel.model_validate(project_obj).model_dump(by_alias=False)
                project_dict.update(
                    {
                        'review_status': row.review_status,
                        'reviewer': row.reviewer,
                        'review_time': row.review_time,
                    }
                )
                rows.append(CamelCaseUtil.transform_result(project_dict))

            has_next = (total + page_object.page_size - 1) // page_object.page_size > page_object.page_num
            return PageModel[Any](
                rows=rows,
                pageNum=page_object.page_num,
                pageSize=page_object.page_size,
                total=total,
                hasNext=has_next,
            )

        query_result = (await db.execute(query)).all()
        data_list: list[dict[str, Any]] = []
        for row in query_result:
            project_obj = row[0]
            project_dict = ProjectModel.model_validate(project_obj).model_dump(by_alias=False)
            project_dict.update(
                {
                    'review_status': row.review_status,
                    'reviewer': row.reviewer,
                    'review_time': row.review_time,
                }
            )
            data_list.append(CamelCaseUtil.transform_result(project_dict))
        return data_list

    # 1. 新增项目（项目创建人新建）
    @classmethod
    async def add_project_dao(cls, db: AsyncSession, project: ProjectModel) -> Project:
        db_project = Project(**project.model_dump())
        db.add(db_project)
        await db.flush()

        return db_project

    @classmethod
    async def delete_pro_dao(cls, db: AsyncSession, project: ProjectModel) -> None:
        """
        删除企业名称数据库操作

        :param db: orm对象
        :param project: 企业名称对象
        :return:
        """
        await db.execute(delete(Project).where(Project.pro_id.in_([project.pro_id])))

    # 2. 修改项目（已归档前均可修改）
    @classmethod
    async def edit_project_dao(cls, db: AsyncSession, project: dict) -> None:
        await db.execute(update(Project), [project])

    # 3. 按project_code查询项目详情
    @classmethod
    async def get_project_by_id(cls, db: AsyncSession, project_code: str) -> Union[Project, None]:
        result = (
            (
                await db.execute(
                    select(Project).where(and_(Project.project_code == project_code, Project.del_flag == '0'))
                )
            )
            .scalars()
            .first()
        )
        return result

    # 3. 按pro_id查询项目详情
    @classmethod
    async def get_project_by_pro_id(cls, db: AsyncSession, pro_id: int) -> Union[Project, None]:
        result = await db.get(Project, pro_id)
        return result

    # @classmethod
    # async def get_project_page_dao(
    #         cls, db: AsyncSession, query_params: dict, data_scope_sql: Any, is_page: bool = True
    # ) -> Union[PageModel, List[Dict[str, Any]]]:
    #     query = (
    #         select(Project)
    #         .where(
    #             and_(
    #                 Project.del_flag == '0',
    #                 Project.project_name.like(f'%{query_params.get("project_name", "")}%') if query_params.get(
    #                     "project_name") else True,
    #                 Project.project_code == query_params.get("project_code") if query_params.get(
    #                     "project_code") else True,
    #                 data_scope_sql  # 角色数据权限SQL（如项目创建人只能看自己创建的项目）
    #             )
    #         )
    #         .order_by(desc(Project.create_time))
    #     )
    #     # 分页处理
    #     project_page = await PageUtil.paginate(
    #         db, query, query_params.get("page_num", 1), query_params.get("page_size", 10), is_page
    #     )
    #     return project_page

    # 5. 软删除项目
    @classmethod
    async def delete_project_dao(cls, db: AsyncSession, project_id: int, update_by: int, update_name: str) -> None:
        await db.execute(
            update(Project)
            .where(Project.pro_id == project_id)
            .values(del_flag='2', update_by=update_by, update_name=update_name)
        )

    @classmethod
    async def batch_add_project_dao(cls, db: AsyncSession, project_list: list[dict[str, Any]]) -> None:
        """
        批量新增项目（基于Excel解析后的项目列表）
        :param db: 数据库
        :param project_list: 项目字典列表（每个字典对应一条项目数据）
        """
        if not project_list:
            return
        # 批量插入SQL（使用SQLAlchemy的insert批量操作）
        await db.execute(insert(Project), project_list)

    # ------------------------------
    # 新增：批量初始化流程（与批量项目对应）
    # ------------------------------
    @classmethod
    async def batch_init_prefect_dao(cls, db: AsyncSession, prefect_list: list[dict[str, Any]]) -> None:
        """
        批量初始化项目流程（每个项目对应一条流程记录，状态：创建人新建）
        :param db: 数据库
        :param prefect_list: 流程字典列表（每个字典对应一条流程数据）
        """
        if not prefect_list:
            return
        await db.execute(insert(ProjectPrefect), prefect_list)

    # ------------------------------
    # 新增：批量查询项目编号（校验Excel中项目编号是否已存在）
    # ------------------------------
    @classmethod
    async def batch_get_project_by_codes(
        cls, db: AsyncSession, project_codes: list[str]
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        """
        批量查询已存在的项目编号（用于Excel导入时的唯一性校验）
        :return: 已存在的项目编号列表
        """
        if not project_codes:
            return []
        result = (
            (
                await db.execute(
                    select(Project.project_code).where(Project.project_code.in_(project_codes), Project.del_flag == '0')
                )
            )
            .scalars()
            .all()
        )
        return result  # 返回已存在的项目编号列表
