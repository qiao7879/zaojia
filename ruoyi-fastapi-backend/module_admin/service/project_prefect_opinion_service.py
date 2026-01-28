from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, List, Dict, Any, Sequence

from exceptions.exception import ServiceException
from module_admin.dao.project_prefect_dao import ProjectPrefectDao
from module_admin.dao.project_prefect_opinion_dao import ProjectPrefectOpinionDao
from module_admin.entity.do.project_prefect_opinion_do import ProjectPrefectOpinion


class ProjectPrefectOpinionService:
    """项目流程意见业务逻辑层"""

    # 1. 查询项目所有历史意见
    @classmethod
    async def get_project_opinions_services(cls, db: AsyncSession, project_id: int) -> list[dict[str, Any]]:
        # 校验：项目是否存在（通过流程表间接校验）

        exist_prefect = await ProjectPrefectDao.get_prefect_by_project_id(db, project_id)
        if not exist_prefect:
            raise ServiceException(message=f'项目ID{project_id}不存在或无流程记录')

        # 查询意见列表
        opinion_list = await ProjectPrefectOpinionDao.get_opinions_by_project_id(db, project_id)
        return opinion_list

    # 2. 查询指定节点的意见（如二级复审意见）
    @classmethod
    async def get_node_opinions_services(cls, db: AsyncSession, project_id: int, node_code: str) -> list[dict[str, Any]]:
        opinion_list = await ProjectPrefectOpinionDao.get_opinions_by_node(db, project_id, node_code)
        if not opinion_list:
            return []
        return opinion_list
