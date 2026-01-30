from typing import Any

from sqlalchemy import and_, delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from module_admin.entity.do.project_prefect_opinion_do import ProjectPrefectOpinion
from module_admin.entity.vo.project_prefect_opinion_vo import ProjectPrefectOpinionModel


class ProjectPrefectOpinionDao:
    """项目流程意见数据访问层"""

    # 1. 新增审核意见（各节点操作时同步新增）
    @classmethod
    async def add_opinion_dao(cls, db: AsyncSession, opinion: dict) -> None:
        db_opinion = ProjectPrefectOpinion(**opinion)
        db.add(db_opinion)

    @classmethod
    async def delete_ent_dao(cls, db: AsyncSession, opinion: ProjectPrefectOpinionModel) -> None:
        """
        删除企业名称数据库操作

        :param db: orm对象
        :param opinion: 企业名称对象
        :return:
        """
        await db.execute(delete(ProjectPrefectOpinion).where(ProjectPrefectOpinion.id.in_([opinion.id])))

    # 2. 按项目ID查询所有历史意见（按时间倒序）
    @classmethod
    async def get_opinions_by_project_id(cls, db: AsyncSession, project_id: int) -> list[dict[str, Any]]:
        result = (
            (
                await db.execute(
                    select(ProjectPrefectOpinion)
                    .where(and_(ProjectPrefectOpinion.project_id == project_id, ProjectPrefectOpinion.del_flag == '0'))
                    .order_by(desc(ProjectPrefectOpinion.create_time))
                )
            )
            .scalars()
            .all()
        )
        if not result:
            return []
        pydantic_rows = [ProjectPrefectOpinionModel.model_validate(orm_obj) for orm_obj in result]
        return [row.model_dump(by_alias=False) for row in pydantic_rows]

    # 3. 按流程节点查询意见（如查询二级复审的所有意见）
    @classmethod
    async def get_opinions_by_node(cls, db: AsyncSession, project_id: int, node_code: str) -> list[dict[str, Any]]:
        result = (
            (
                await db.execute(
                    select(ProjectPrefectOpinion).where(
                        and_(
                            ProjectPrefectOpinion.project_id == project_id,
                            ProjectPrefectOpinion.node_code == node_code,
                            ProjectPrefectOpinion.del_flag == '0',
                        )
                    )
                )
            )
            .scalars()
            .all()
        )
        if not result:
            return []
        pydantic_rows = [ProjectPrefectOpinionModel.model_validate(orm_obj) for orm_obj in result]
        return [row.model_dump(by_alias=False) for row in pydantic_rows]
