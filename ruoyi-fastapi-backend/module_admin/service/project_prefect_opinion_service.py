from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, List, Dict, Any
from app.modules.project.dao.project_prefect_opinion_dao import ProjectPrefectOpinionDao
from app.common.exception.service_exception import ServiceException


class ProjectPrefectOpinionService:
    """项目流程意见业务逻辑层"""

    # 1. 查询项目所有历史意见
    @classmethod
    async def get_project_opinions_services(cls, db: AsyncSession, project_id: int) -> List[Dict[str, Any]]:
        # 校验：项目是否存在（通过流程表间接校验）
        from app.modules.project.dao.project_prefect_dao import ProjectPrefectDao
        exist_prefect = await ProjectPrefectDao.get_prefect_by_project_id(db, project_id)
        if not exist_prefect:
            raise ServiceException(message=f'项目ID{project_id}不存在或无流程记录')

        # 查询意见列表
        opinion_list = await ProjectPrefectOpinionDao.get_opinions_by_project_id(db, project_id)
        return opinion_list

    # 2. 查询指定节点的意见（如二级复审意见）
    @classmethod
    async def get_node_opinions_services(cls, db: AsyncSession, project_id: int, node_code: str) -> List[
        Dict[str, Any]]:
        opinion_list = await ProjectPrefectOpinionDao.get_opinions_by_node(db, project_id, node_code)
        if not opinion_list:
            return []
        return opinion_list
