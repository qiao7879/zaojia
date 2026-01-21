from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, and_, desc
from typing import Union, List, Dict, Any

from module_admin.entity.do.project_prefect_opinion_do import SysProjectPrefectOpinion
from module_admin.entity.vo.project_prefect_opinion_vo import AddPrefectOpinionModel


class ProjectPrefectOpinionDao:
    """项目流程意见数据访问层"""

    # 1. 新增审核意见（各节点操作时同步新增）
    @classmethod
    async def add_opinion_dao(cls, db: AsyncSession, opinion: AddPrefectOpinionModel) -> None:
        db_opinion = SysProjectPrefectOpinion(**opinion.model_dump(exclude_unset=True))
        db.add(db_opinion)

    # 2. 按项目ID查询所有历史意见（按时间倒序）
    @classmethod
    async def get_opinions_by_project_id(cls, db: AsyncSession, project_id: int) -> List[Dict[str, Any]]:
        result = (
            await db.execute(
                select(SysProjectPrefectOpinion)
                .where(
                    and_(SysProjectPrefectOpinion.project_id == project_id, SysProjectPrefectOpinion.del_flag == '0'))
                .order_by(desc(SysProjectPrefectOpinion.create_time))
            )
        ).scalars().all()
        # 转换为字典列表返回
        return [opinion.__dict__ for opinion in result] if result else []

    # 3. 按流程节点查询意见（如查询二级复审的所有意见）
    @classmethod
    async def get_opinions_by_node(cls, db: AsyncSession, project_id: int, node_code: str) -> List[Dict[str, Any]]:
        result = (
            await db.execute(
                select(SysProjectPrefectOpinion)
                .where(
                    and_(
                        SysProjectPrefectOpinion.project_id == project_id,
                        SysProjectPrefectOpinion.node_code == node_code,
                        SysProjectPrefectOpinion.del_flag == '0'
                    )
                )
            )
        ).scalars().all()
        return [opinion.__dict__ for opinion in result] if result else []
