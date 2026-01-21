from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, List, Dict, Any
from app.modules.project.dao.project_prefect_dao import ProjectPrefectDao
from app.modules.project.dao.project_prefect_opinion_dao import ProjectPrefectOpinionDao
from app.modules.project.model.project_prefect_vo import UpdatePrefectStatusModel
from app.modules.project.model.project_prefect_do import PREFECT_STATUS_ENUM
from app.common.model.crud_response_model import CrudResponseModel
from app.common.exception.service_exception import ServiceException
from app.common.constant.role_constant import RoleConstant


class ProjectPrefectService:
    """项目流程业务逻辑层（核心流程控制）"""

    # 1. 项目创建人下发项目至工程师
    @classmethod
    async def creator_send_to_engineer_services(
            cls, db: AsyncSession, prefect: UpdatePrefectStatusModel, current_user: dict
    ) -> CrudResponseModel:
        try:
            # 校验：角色（仅项目创建人）
            if current_user["role"] != RoleConstant.PROJECT_CREATOR:
                raise ServiceException(message='仅项目创建人可下发项目至工程师')

            # 校验：当前流程状态（必须是"项目创建人新建"）
            exist_prefect = await ProjectPrefectDao.get_prefect_by_project_id(db, prefect.project_id)
            if not exist_prefect or exist_prefect.current_status != PREFECT_STATUS_ENUM["CREATE"]:
                raise ServiceException(message='当前流程状态不允许下发，仅新建项目可下发')

            # 1. 更新流程状态（目标状态：工程师修改）
            prefect.target_status = PREFECT_STATUS_ENUM["ENGINEER_EDIT"]
            await ProjectPrefectDao.update_prefect_status_dao(db, prefect)

            # 2. 新增审核意见（项目创建人下发意见）
            opinion_data = {
                "project_id": prefect.project_id,
                "prefect_id": exist_prefect.id,
                "node_code": PREFECT_STATUS_ENUM["CREATE"],
                "node_name": "项目创建人下发",
                "opinion_content": prefect.opinion_content,
                "operator_id": current_user["user_id"],
                "operator_name": current_user["user_name"],
                "operator_role": current_user["role"]
            }
            await ProjectPrefectOpinionDao.add_opinion_dao(db, opinion_data)

            await db.commit()
            return CrudResponseModel(is_success=True, message='项目已下发至工程师')
        except Exception as e:
            await db.rollback()
            raise e

    # 2. 工程师修改后提交审核（目标状态：二级复审）
    @classmethod
    async def engineer_submit_review_services(
            cls, db: AsyncSession, prefect: UpdatePrefectStatusModel, current_user: dict
    ) -> CrudResponseModel:
        try:
            # 校验：角色（仅工程师）
            if current_user["role"] != RoleConstant.ENGINEER:
                raise ServiceException(message='仅工程师可提交审核')

            # 校验：当前流程状态（必须是"工程师修改中"）
            exist_prefect = await ProjectPrefectDao.get_prefect_by_project_id(db, prefect.project_id)
            if not exist_prefect or exist_prefect.current_status != PREFECT_STATUS_ENUM["ENGINEER_EDIT"]:
                raise ServiceException(message='当前流程状态不允许提交，仅工程师修改中可提交')

            # 1. 更新流程状态（目标状态：二级复审，自动显示开票用章按钮）
            prefect.target_status = PREFECT_STATUS_ENUM["SECOND_REVIEW"]
            await ProjectPrefectDao.update_prefect_status_dao(db, prefect)

            # 2. 新增审核意见（工程师修改说明）
            opinion_data = {
                "project_id": prefect.project_id,
                "prefect_id": exist_prefect.id,
                "node_code": PREFECT_STATUS_ENUM["ENGINEER_EDIT"],
                "node_name": "工程师修改",
                "opinion_content": prefect.opinion_content,
                "operator_id": current_user["user_id"],
                "operator_name": current_user["user_name"],
                "operator_role": current_user["role"]
            }
            await ProjectPrefectOpinionDao.add_opinion_dao(db, opinion_data)

            await db.commit()
            return CrudResponseModel(is_success=True, message='项目已提交至二级复审')
        except Exception as e:
            await db.rollback()
            raise e

    # 3. 二级复审操作（通过→三级复审；驳回→工程师）
    @classmethod
    async def second_review_services(
            cls, db: AsyncSession, prefect: UpdatePrefectStatusModel, current_user: dict
    ) -> CrudResponseModel:
        try:
            # 校验：角色（仅二级复核）
            if current_user["role"] != RoleConstant.SECOND_REVIEWER:
                raise ServiceException(message='仅二级复核可执行此操作')

            # 校验：当前流程状态（必须是"二级复审"）
            exist_prefect = await ProjectPrefectDao.get_prefect_by_project_id(db, prefect.project_id)
            if not exist_prefect or exist_prefect.current_status != PREFECT_STATUS_ENUM["SECOND_REVIEW"]:
                raise ServiceException(message='当前流程状态不允许复审，仅二级复审中可操作')

            # 校验：目标状态合法（仅允许三级复审/驳回至工程师）
            if prefect.target_status not in [PREFECT_STATUS_ENUM["THIRD_REVIEW"],
                                             PREFECT_STATUS_ENUM["REJECT_ENGINEER"]]:
                raise ServiceException(message='二级复审仅允许流转至三级复审或驳回至工程师')

            # 1. 更新流程状态
            await ProjectPrefectDao.update_prefect_status_dao(db, prefect)

            # 2. 新增审核意见（二级复审意见）
            opinion_data = {
                "project_id": prefect.project_id,
                "prefect_id": exist_prefect.id,
                "node_code": PREFECT_STATUS_ENUM["SECOND_REVIEW"],
                "node_name": "二级复审",
                "opinion_content": prefect.opinion_content,
                "operator_id": current_user["user_id"],
                "operator_name": current_user["user_name"],
                "operator_role": current_user["role"]
            }
            await ProjectPrefectOpinionDao.add_opinion_dao(db, opinion_data)

            await db.commit()
            msg = "二级复审通过，流转至三级复审" if prefect.target_status == PREFECT_STATUS_ENUM[
                "THIRD_REVIEW"] else "二级复审驳回至工程师"
            return CrudResponseModel(is_success=True, message=msg)
        except Exception as e:
            await db.rollback()
            raise e

    # 4. 三级复审操作（通过→待归档；驳回→工程师）
    @classmethod
    async def third_review_services(
            cls, db: AsyncSession, prefect: UpdatePrefectStatusModel, current_user: dict
    ) -> CrudResponseModel:
        try:
            # 校验：角色（仅三级复核）
            if current_user["role"] != RoleConstant.THIRD_REVIEWER:
                raise ServiceException(message='仅三级复核可执行此操作')

            # 校验：当前流程状态（必须是"三级复审"）
            exist_prefect = await ProjectPrefectDao.get_prefect_by_project_id(db, prefect.project_id)
            if not exist_prefect or exist_prefect.current_status != PREFECT_STATUS_ENUM["THIRD_REVIEW"]:
                raise ServiceException(message='当前流程状态不允许复审，仅三级复审中可操作')

            # 校验：目标状态合法（仅允许待归档/驳回至工程师）
            if prefect.target_status not in [PREFECT_STATUS_ENUM["TO_ARCHIVE"], PREFECT_STATUS_ENUM["REJECT_ENGINEER"]]:
                raise ServiceException(message='三级复审仅允许流转至待归档或驳回至工程师')

            # 1. 更新流程状态
            await ProjectPrefectDao.update_prefect_status_dao(db, prefect)

            # 2. 新增审核意见（三级复审意见）
            opinion_data = {
                "project_id": prefect.project_id,
                "prefect_id": exist_prefect.id,
                "node_code": PREFECT_STATUS_ENUM["THIRD_REVIEW"],
                "node_name": "三级复审",
                "opinion_content": prefect.opinion_content,
                "operator_id": current_user["user_id"],
                "operator_name": current_user["user_name"],
                "operator_role": current_user["role"]
            }
            await ProjectPrefectOpinionDao.add_opinion_dao(db, opinion_data)

            await db.commit()
            msg = "三级复审通过，流转至待归档" if prefect.target_status == PREFECT_STATUS_ENUM[
                "TO_ARCHIVE"] else "三级复审驳回至工程师"
            return CrudResponseModel(is_success=True, message=msg)
        except Exception as e:
            await db.rollback()
            raise e

    # 5. 归档人员执行归档（待归档→已归档，流程结束）
    @classmethod
    async def archive_project_services(
            cls, db: AsyncSession, prefect: UpdatePrefectStatusModel, current_user: dict
    ) -> CrudResponseModel:
        try:
            # 校验：角色（仅归档人员）
            if current_user["role"] != RoleConstant.ARCHIVER:
                raise ServiceException(message='仅归档人员可执行归档操作')

            # 校验：当前流程状态（必须是"待归档"）
            exist_prefect = await ProjectPrefectDao.get_prefect_by_project_id(db, prefect.project_id)
            if not exist_prefect or exist_prefect.current_status != PREFECT_STATUS_ENUM["TO_ARCHIVE"]:
                raise ServiceException(message='当前流程状态不允许归档，仅待归档项目可操作')

            # 1. 更新流程状态（目标状态：已归档）
            prefect.target_status = PREFECT_STATUS_ENUM["ARCHIVED"]
            await ProjectPrefectDao.update_prefect_status_dao(db, prefect)

            # 2. 新增审核意见（归档意见）
            opinion_data = {
                "project_id": prefect.project_id,
                "prefect_id": exist_prefect.id,
                "node_code": PREFECT_STATUS_ENUM["TO_ARCHIVE"],
                "node_name": "归档操作",
                "opinion_content": prefect.opinion_content,
                "operator_id": current_user["user_id"],
                "operator_name": current_user["user_name"],
                "operator_role": current_user["role"]
            }
            await ProjectPrefectOpinionDao.add_opinion_dao(db, opinion_data)

            await db.commit()
            return CrudResponseModel(is_success=True, message='项目归档成功，流程结束')
        except Exception as e:
            await db.rollback()
            raise e

    # 6. 归档人员查询待归档项目列表
    @classmethod
    async def get_to_archive_projects_services(
            cls, db: AsyncSession, page_num: int, page_size: int, current_user: dict
    ) -> Dict[str, Any]:
        # 校验：角色（仅归档人员）
        if current_user["role"] != RoleConstant.ARCHIVER:
            raise ServiceException(message='仅归档人员可查看待归档项目')

        to_archive_page = await ProjectPrefectDao.get_to_archive_projects_dao(db, page_num, page_size)
        return to_archive_page.__dict__ if hasattr(to_archive_page, '__dict__') else to_archive_page
