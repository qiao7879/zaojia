from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, func, desc, insert
from typing import Union, List, Dict, Any

from common.vo import PageModel
from module_admin.entity.do.project_do import SysProject
from module_admin.entity.do.project_prefect_do import SysProjectPrefect
from module_admin.entity.vo.project_vo import AddProjectModel, EditProjectModel
from utils.page_util import PageUtil



class ProjectDao:
    """项目主表数据访问层"""

    # 1. 新增项目（项目创建人新建）
    @classmethod
    async def add_project_dao(cls, db: AsyncSession, project: AddProjectModel) -> SysProject:
        db_project = SysProject(**project.model_dump(exclude_unset=True))
        db.add(db_project)
        await db.flush()
        return db_project

    # 2. 修改项目（已归档前均可修改）
    @classmethod
    async def edit_project_dao(cls, db: AsyncSession, project: EditProjectModel) -> None:
        update_data = project.model_dump(exclude_unset=True, exclude={'id'})
        await db.execute(
            update(SysProject)
            .where(and_(SysProject.id == project.id, SysProject.del_flag == '0'))
            .values(update_data)
        )

    # 3. 按ID查询项目详情
    @classmethod
    async def get_project_by_id(cls, db: AsyncSession, project_id: int) -> Union[SysProject, None]:
        result = (
            await db.execute(
                select(SysProject)
                .where(and_(SysProject.id == project_id, SysProject.del_flag == '0'))
            )
        ).scalars().first()
        return result

    # 4. 分页查询项目列表（支持角色数据权限）
    @classmethod
    async def get_project_page_dao(
            cls, db: AsyncSession, query_params: dict, data_scope_sql: Any, is_page: bool = True
    ) -> Union[PageModel, List[Dict[str, Any]]]:
        query = (
            select(SysProject)
            .where(
                and_(
                    SysProject.del_flag == '0',
                    SysProject.project_name.like(f'%{query_params.get("project_name", "")}%') if query_params.get(
                        "project_name") else True,
                    SysProject.project_code == query_params.get("project_code") if query_params.get(
                        "project_code") else True,
                    data_scope_sql  # 角色数据权限SQL（如项目创建人只能看自己创建的项目）
                )
            )
            .order_by(desc(SysProject.create_time))
        )
        # 分页处理
        project_page = await PageUtil.paginate(
            db, query, query_params.get("page_num", 1), query_params.get("page_size", 10), is_page
        )
        return project_page

    # 5. 软删除项目
    @classmethod
    async def delete_project_dao(cls, db: AsyncSession, project_id: int, update_by: int, update_name: str) -> None:
        await db.execute(
            update(SysProject)
            .where(SysProject.id == project_id)
            .values(del_flag='2', update_by=update_by, update_name=update_name)
        )

    @classmethod
    async def batch_add_project_dao(cls, db: AsyncSession, project_list: List[Dict[str, Any]]) -> None:
        """
        批量新增项目（基于Excel解析后的项目列表）
        :param project_list: 项目字典列表（每个字典对应一条项目数据）
        """
        if not project_list:
            return
        # 批量插入SQL（使用SQLAlchemy的insert批量操作）
        await db.execute(insert(SysProject), project_list)

    # ------------------------------
    # 新增：批量初始化流程（与批量项目对应）
    # ------------------------------
    @classmethod
    async def batch_init_prefect_dao(cls, db: AsyncSession, prefect_list: List[Dict[str, Any]]) -> None:
        """
        批量初始化项目流程（每个项目对应一条流程记录，状态：创建人新建）
        :param prefect_list: 流程字典列表（每个字典对应一条流程数据）
        """
        if not prefect_list:
            return
        await db.execute(insert(SysProjectPrefect), prefect_list)

    # ------------------------------
    # 新增：批量查询项目编号（校验Excel中项目编号是否已存在）
    # ------------------------------
    @classmethod
    async def batch_get_project_by_codes(cls, db: AsyncSession, project_codes: List[str]) -> List[str]:
        """
        批量查询已存在的项目编号（用于Excel导入时的唯一性校验）
        :return: 已存在的项目编号列表
        """
        if not project_codes:
            return []
        result = (
            await db.execute(
                select(SysProject.project_code)
                .where(SysProject.project_code.in_(project_codes), SysProject.del_flag == '0')
            )
        ).scalars().all()
        return result  # 返回已存在的项目编号列表
