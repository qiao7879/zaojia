from typing import Any

from sqlalchemy import and_, delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_admin.entity.do.project_do import Project
from module_admin.entity.do.project_prefect_do import PREFECT_STATUS_ENUM, ProjectPrefect
from module_admin.entity.vo.project_prefect_vo import ProjectPrefectModel, UpdatePrefectStatusModel
from utils.page_util import PageUtil


class ProjectPrefectDao:
    """项目流程数据访问层"""

    # 1. 初始化流程（项目创建人新建项目时同步创建流程）
    @classmethod
    async def init_prefect_dao(cls, db: AsyncSession, prefect: ProjectPrefectModel) -> ProjectPrefect:
        db_prefect = ProjectPrefect(**prefect.model_dump())
        db.add(db_prefect)
        await db.flush()
        return db_prefect

    @classmethod
    async def delete_ent_dao(cls, db: AsyncSession, prefect: ProjectPrefectModel) -> None:
        """
        删除企业名称数据库操作

        :param db: orm对象
        :param prefect: 企业名称对象
        :return:
        """
        await db.execute(delete(ProjectPrefect).where(ProjectPrefect.id.in_([prefect.id])))

    # 2. 更新流程状态（含"开票/用章"按钮显示控制）
    @classmethod
    async def update_prefect_status_dao(cls, db: AsyncSession, prefect: UpdatePrefectStatusModel) -> None:
        # 二级/三级复审时显示开票用章按钮，其他节点不显示
        show_invoice_seal = (
            '1'
            if prefect.target_status in [PREFECT_STATUS_ENUM['SECOND_REVIEW'], PREFECT_STATUS_ENUM['THIRD_REVIEW']]
            else '0'
        )
        await db.execute(
            update(ProjectPrefect)
            .where(and_(ProjectPrefect.pro_id == prefect.pro_id, ProjectPrefect.del_flag == '0'))
            .values(
                current_status=prefect.target_status,
                show_invoice_seal=show_invoice_seal,
                operator_id=prefect.operator_id,
                operator_name=prefect.operator_name,
                update_time=func.now(),
            )
        )
        await db.execute(
            update(Project)
            .where(Project.pro_id == prefect.pro_id)
            .values(prefect_status=prefect.target_status, update_time=func.now())
        )

    # # 3. 按项目ID查询当前流程状态
    @classmethod
    async def get_prefect_by_project_id(cls, db: AsyncSession, project_id: int) -> ProjectPrefect | None:
        result = (
            (
                await db.execute(
                    select(ProjectPrefect)
                    .where(and_(ProjectPrefect.pro_id == project_id, ProjectPrefect.del_flag == '0'))
                    .order_by(desc(ProjectPrefect.update_time))
                )
            )
            .scalars()
            .first()
        )
        return result

    @classmethod
    async def get_prefects_by_project_ids(cls, db: AsyncSession, project_ids: list[int]) -> dict[int, ProjectPrefect]:
        if not project_ids:
            return {}
        result = (
            (
                await db.execute(
                    select(ProjectPrefect)
                    .where(and_(ProjectPrefect.pro_id.in_(project_ids), ProjectPrefect.del_flag == '0'))
                    .order_by(ProjectPrefect.pro_id.asc(), desc(ProjectPrefect.update_time))
                )
            )
            .scalars()
            .all()
        )
        prefect_map: dict[int, ProjectPrefect] = {}
        for row in result:
            if row.pro_id not in prefect_map:
                prefect_map[row.pro_id] = row
        return prefect_map

    # 4. 分页查询待归档项目（归档人员专用）
    @classmethod
    async def get_to_archive_projects_dao(
        cls, db: AsyncSession, page_num: int, page_size: int
    ) -> PageModel | list[dict[str, Any]]:
        query = (
            select(ProjectPrefect, Project)
            .join(Project, ProjectPrefect.pro_id == Project.pro_id)
            .where(
                and_(
                    ProjectPrefect.current_status == PREFECT_STATUS_ENUM['TO_ARCHIVE'],
                    ProjectPrefect.del_flag == '0',
                    Project.del_flag == '0',
                )
            )
            .order_by(desc(ProjectPrefect.update_time))
        )
        to_archive_page = await PageUtil.paginate(db, query, page_num, page_size, is_page=True)
        return to_archive_page

    @classmethod
    async def get_project_prefect_by_pro_id(cls, query_db: AsyncSession, pro_id: int) -> ProjectPrefect | None:
        result = (
            (
                await query_db.execute(
                    select(ProjectPrefect)
                    .where(and_(ProjectPrefect.pro_id == pro_id, ProjectPrefect.del_flag == '0'))
                    .order_by(desc(ProjectPrefect.update_time))
                )
            )
            .scalars()
            .first()
        )
        return result
