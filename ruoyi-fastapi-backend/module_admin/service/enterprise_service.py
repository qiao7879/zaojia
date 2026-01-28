from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from common.constant import CommonConstant
from common.vo import CrudResponseModel
from exceptions.exception import ServiceException
from module_admin.dao.enterprise_info_dao import EnterpriseDao
from module_admin.entity.do.enterprise_info_do import Enterprise
from module_admin.entity.vo.enterprise_info_vo import EnterpriseQueryModel, EnterpriseModel, DeleteEnterpriseModel, \
    EnterprisePageModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from utils.common_util import CamelCaseUtil



class EnterpriseService:
    """
    单位管理模块服务层
    """



    @classmethod
    async def get_ent_list_services(
        cls, query_db: AsyncSession, page_object: EnterprisePageModel, is_page: bool = False) -> list[dict[str, Any]]:
        """
        获取单位列表信息service

        :param query_db: orm对象
        :param page_object: 分页查询参数对象
        :param is_page: 是否分页查询
        :return: 单位列表信息对象
        """
        menu_list_result = await EnterpriseDao.get_ent_list(
            query_db, page_object, is_page
        )

        return CamelCaseUtil.transform_result(menu_list_result)

    @classmethod
    async def check_ent_name_unique_services(cls, query_db: AsyncSession, page_object: EnterpriseModel) -> bool:
        """
        校验单位名称是否唯一service

        :param query_db: orm对象
        :param page_object: 单位对象
        :return: 校验结果
        """
        ent_id = -1 if page_object.ent_id is None else page_object.ent_id
        menu = await EnterpriseDao.get_ent_detail_by_info(query_db, EnterpriseModel(menuName=page_object.menu_name))
        if menu and menu.ent_id != ent_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def add_ent_services(cls, query_db: AsyncSession, page_object: EnterpriseModel) -> CrudResponseModel:
        """
        新增单位信息service

        :param query_db: orm对象
        :param page_object: 新增单位对象
        :return: 新增单位校验结果
        """
        try:
            user_info = EnterpriseModel(**page_object.model_dump(by_alias=True))
            await EnterpriseDao.add_ent_dao(query_db, user_info)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_ent_services(cls, query_db: AsyncSession, page_object: EnterpriseModel) -> CrudResponseModel:
        """
        编辑单位信息service

        :param query_db: orm对象
        :param page_object: 编辑部门对象
        :return: 编辑单位校验结果
        """
        edit_menu = page_object.model_dump(exclude_unset=True)
        ent_info = await cls.ent_detail_services(query_db, page_object.ent_id)
        if ent_info.ent_id:
            if page_object.taxpayer_id != ent_info.taxpayer_id:  # 只有当taxpayer_id发生变化时才校验
                duplicate_ent = await query_db.execute(
                    # 条件：taxpayer_id匹配 + ent_id不匹配（排除自身）
                    select(Enterprise).where(
                        Enterprise.taxpayer_id == page_object.taxpayer_id,
                        Enterprise.ent_id != page_object.ent_id
                    )
                )
                duplicate_ent_obj = duplicate_ent.scalars().first()
                if duplicate_ent_obj:
                    return CrudResponseModel(
                        is_success=False,
                        message=f"纳税人识别号 {page_object.taxpayer_id} 已被其他企业占用，无法更新"
                    )

                try:
                    await EnterpriseDao.edit_ent_dao(query_db, edit_menu)
                    await query_db.commit()
                    return CrudResponseModel(is_success=True, message='更新成功')
                except Exception as e:
                    await query_db.rollback()
                    raise e
            else:
                raise ServiceException(message='纳税人编号重复')
        else:
            raise ServiceException(message='单位不存在')

    @classmethod
    async def delete_ent_services(cls, query_db: AsyncSession, page_object: DeleteEnterpriseModel) -> CrudResponseModel:
        """
        删除单位信息service

        :param query_db: orm对象
        :param page_object: 删除单位对象
        :return: 删除单位校验结果
        """
        if page_object.ent_ids:
            ent_id_list = page_object.ent_ids.split(',')
            try:
                for ent_id in ent_id_list:
                    await EnterpriseDao.delete_ent_dao(query_db, EnterpriseModel(entId=ent_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入单位id为空')

    @classmethod
    async def ent_detail_services(cls, query_db: AsyncSession, ent_id: int) -> EnterpriseModel:
        """
        获取单位详细信息service

        :param query_db: orm对象
        :param ent_id: 单位id
        :return: 单位id对应的信息
        """
        menu = await EnterpriseDao.get_ent_detail_by_id(query_db, ent_id=ent_id)
        result = EnterpriseModel(**CamelCaseUtil.transform_result(menu)) if menu else EnterpriseModel()

        return result


