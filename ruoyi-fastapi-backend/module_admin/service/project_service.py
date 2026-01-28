from io import BytesIO

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, List, Dict, Any, Optional

from common.vo import CrudResponseModel
from exceptions.exception import ServiceException
from module_admin.dao.enterprise_info_dao import EnterpriseDao
from module_admin.dao.project_dao import ProjectDao
from module_admin.dao.project_prefect_dao import ProjectPrefectDao
from module_admin.dao.project_prefect_opinion_dao import ProjectPrefectOpinionDao
# from module_admin.entity.do.project_do import Project
from module_admin.entity.do.project_prefect_do import PREFECT_STATUS_ENUM
from module_admin.entity.vo.project_prefect_vo import ProjectPrefectModel
from module_admin.entity.vo.project_vo import AddProjectModel, EditProjectModel, ProjectModel, \
    DeleteProjectModel, ProjectPageModel, ProjectDetailModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.project_prefect_opinion_service import ProjectPrefectOpinionService
from utils.common_util import CamelCaseUtil


# from module_admin.service.dept_service import DeptService


class ProjectService:
    """项目主表业务逻辑层"""

    @classmethod
    async def get_project_list_services(
            cls, query_db: AsyncSession, page_object: ProjectPageModel, is_page: bool = False) -> list[
        dict[str, Any]]:
        """
        获取单位列表信息service

        :param query_db: orm对象
        :param page_object: 分页查询参数对象
        :param is_page: 是否分页查询
        :return: 单位列表信息对象
        """
        menu_list_result = await ProjectDao.get_project_list(
            query_db, page_object, is_page
        )

        return CamelCaseUtil.transform_result(menu_list_result)

    # 1. 项目创建人新建项目（同步初始化流程）
    @classmethod
    async def add_project_services(
            cls, db: AsyncSession, project: AddProjectModel
    ) -> CrudResponseModel:
        try:
            # 校验：项目创建人角色
            # if current_user["role"] != RoleConstant.PROJECT_CREATOR:
            #     raise ServiceException(message='仅项目创建人可新建项目')

            # 校验：项目编号唯一
            exist_project = await ProjectDao.get_project_by_id(db, project.project_code)
            if exist_project:
                raise ServiceException(message=f'项目编号{project.project_code}已存在')

            # 校验企业ID是否存在
            if project.ent_id:
                enterprise_exists = await EnterpriseDao.get_ent_detail_by_id(db, project.ent_id)
                if not enterprise_exists:
                    raise ServiceException(message=f'企业ID {project.ent_id} 不存在')

            # 1. 新增项目主表
            project_info = ProjectModel(**project.model_dump(by_alias=True))
            add_result = await ProjectDao.add_project_dao(db, project_info)

            # 2. 同步初始化流程（状态：项目创建人新建）
            prefect_data = {
                "proId": add_result.pro_id,
                "currentStatus": PREFECT_STATUS_ENUM["CREATE"],
                "operatorId": project.create_by,
                "operatorName": project.create_name
            }

            await ProjectPrefectDao.init_prefect_dao(db, ProjectPrefectModel(**prefect_data))

            await db.commit()
            return CrudResponseModel(is_success=True, message='项目新建成功')
        except Exception as e:
            await db.rollback()
            raise e

    @classmethod
    async def project_detail_services(cls, query_db: AsyncSession, pro_id: int) -> ProjectDetailModel:
        """
        获取项目详细信息service（含所有字段 + 不修改工具类）
        """
        project = await ProjectDao.get_project_by_pro_id(query_db, pro_id=pro_id)

        if project:
            # 手动构造包含所有字段的字典（完全匹配日志中的字段，无遗漏）
            project_dict = {
                # 基础标识字段
                "pro_id": project.pro_id,
                "project_code": project.project_code,
                "project_name": project.project_name,
                "project_type": project.project_type,
                "ent_id": project.ent_id,
                "ent_name": project.ent_name,

                # 项目信息字段
                "service_content": project.service_content,
                "user_company": project.user_company,
                "project_manager": project.project_manager,
                "coordinator": project.coordinator,
                "contract_signed": project.contract_signed,
                "document_obtained": project.document_obtained,
                "contract_amount": project.contract_amount,
                "contract_discount": project.contract_discount,
                "deliverable_completed": project.deliverable_completed,
                "control_price_review": project.control_price_review,

                # 结算相关字段
                "settlement_submitted": project.settlement_submitted,
                "settlement_approved": project.settlement_approved,
                "invoice_should_amount": project.invoice_should_amount,
                "payment_applied": project.payment_applied,
                "payment_month": project.payment_month,

                # 发票相关字段
                "invoice_issued": project.invoice_issued,
                "invoice_date": project.invoice_date,
                "invoice_issued_amount": project.invoice_issued_amount,
                "invoice_remaining_amount": project.invoice_remaining_amount,

                # 收款相关字段
                "payment_received": project.payment_received,
                "payment_received_amount": project.payment_received_amount,
                "payment_received_date": project.payment_received_date,
                "payment_remaining_amount": project.payment_remaining_amount,
                "payment_recovery_rate": project.payment_recovery_rate,

                # 对账相关字段
                "reconciliation_done": project.reconciliation_done,
                "reconciliation_date": project.reconciliation_date,
                "reconciliation_voucher": project.reconciliation_voucher,

                # 佣金相关字段
                "commission_accrued": project.commission_accrued,
                "commission_amount": project.commission_amount,
                "commission_date": project.commission_date,

                # 文件/凭证相关字段
                "contract_electronic_saved": project.contract_electronic_saved,
                "contract_file": project.contract_file,
                "deliverable_electronic_saved": project.deliverable_electronic_saved,
                "deliverable_file": project.deliverable_file,
                "document_paper_saved": project.document_paper_saved,
                "document_save_type": project.document_save_type,

                # 辅助字段
                "remarks": project.remarks,
                "start_date": project.start_date,
                "end_date": project.end_date,
                "project_budget": project.project_budget,
                "project_desc": project.project_desc,
                "status": project.status,
                "prefect_status": project.prefect_status,  # 需确保模型中max_length=255

                # 审计字段
                "create_by": project.create_by,
                "create_name": project.create_name,
                "create_time": project.create_time,
                "update_by": project.update_by,
                "update_name": project.update_name,
                "update_time": project.update_time,
                "del_flag": project.del_flag
            }
            # 用包含所有字段的字典初始化模型（解包合法，字段无遗漏）
            result = ProjectModel(**project_dict)
        else:
            # 无数据时返回空模型（所有字段为默认值/None）
            result = ProjectDetailModel()

        return result

    @classmethod
    async def edit_project_services(cls, query_db: AsyncSession, page_object: EditProjectModel) -> CrudResponseModel:
        """
        编辑单位信息service

        :param query_db: orm对象
        :param page_object: 编辑部门对象
        :return: 编辑单位校验结果
        """
        edit_menu = page_object.model_dump(exclude_unset=True)

        project_info = await ProjectDao.get_project_by_pro_id(query_db, pro_id=page_object.pro_id)

        project_code = await ProjectDao.get_project_by_id(query_db, project_code=page_object.project_code)

        if project_info.pro_id:
            if project_info.prefect_status == PREFECT_STATUS_ENUM["ARCHIVED"]:
                raise ServiceException(message='项目已归档，不可修改')

            if project_info.project_code != page_object.project_code:
                if project_code:
                    raise ServiceException(message=f'项目编号{page_object.project_code}已存在')

            try:
                await ProjectDao.edit_project_dao(query_db, edit_menu)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e

        else:
            raise ServiceException(message='项目不存在')



    @classmethod
    async def delete_project_services(cls, query_db: AsyncSession, page_object: DeleteProjectModel) -> CrudResponseModel:
        """
        删除单位信息service

        :param query_db: orm对象
        :param page_object: 删除单位对象
        :return: 删除单位校验结果
        """
        if page_object.pro_ids:
            ent_id_list = page_object.pro_ids.split(',')
            try:
                for pro_id in ent_id_list:
                    await ProjectDao.delete_pro_dao(query_db, ProjectModel(proId=pro_id))

                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入单位id为空')



    # 2. 修改项目（已归档前均可修改）
    # @classmethod
    # async def edit_project_services(
    #         cls, db: AsyncSession, project: EditProjectModel) -> CrudResponseModel:
    #     try:
    #         # 校验：项目是否存在
    #         exist_project = await ProjectDao.get_project_by_id(db, project.id)
    #         if not exist_project:
    #             raise ServiceException(message=f'项目ID{project.id}不存在')
    #
    #         # 校验：项目是否已归档（已归档不可修改）
    #         prefect_info = await ProjectPrefectDao.get_prefect_by_project_id(db, project.id)
    #         if prefect_info and prefect_info.current_status == PREFECT_STATUS_ENUM["ARCHIVED"]:
    #             raise ServiceException(message='项目已归档，不可修改')

    # 校验：角色权限（项目创建人/工程师/项目成员可修改）
    # allow_roles = [RoleConstant.PROJECT_CREATOR, RoleConstant.ENGINEER, RoleConstant.PROJECT_MEMBER]
    # if current_user["role"] not in allow_roles:
    #     raise ServiceException(message='仅项目创建人、工程师、项目成员可修改项目')

    # 补充更新人信息
    # project.update_by = current_user["user_id"]
    # project.update_name = current_user["user_name"]

    # 执行修改
    #     await ProjectDao.edit_project_dao(db, project)
    #     await db.commit()
    #     return CrudResponseModel(is_success=True, message='项目修改成功')
    # except Exception as e:
    #     await db.rollback()
    #     raise e

    # 3. 查询项目详情（含流程状态、历史意见）
    @classmethod
    async def get_project_detail_services(cls, db: AsyncSession, project_id: int) -> Dict[str, Any]:
        # 1. 查询项目基础信息
        project_info = await ProjectDao.get_project_by_pro_id(db, project_id)
        if not project_info:
            raise ServiceException(message=f'项目ID{project_id}不存在')

        # 2. 查询流程状态信息（是否显示开票用章按钮）
        prefect_info = await ProjectPrefectDao.get_prefect_by_project_id(db, project_id)
        prefect_dict = {
            "current_status": prefect_info.current_status,
            "current_status_name": {v: k for k, v in PREFECT_STATUS_ENUM.items()}[prefect_info.current_status],
            "show_invoice_seal": prefect_info.show_invoice_seal
        } if prefect_info else {}

        # 3. 查询历史审核意见
        opinion_list = await ProjectPrefectOpinionDao.get_opinions_by_project_id(db, project_id)

        # 分别转换每个数据结构为驼峰格式
        project_data = {}
        if project_info:
            # 使用 Pydantic 模型转换而不是直接访问 __dict__
            project_model = ProjectModel.model_validate(project_info)
            project_data = project_model.model_dump(by_alias=False)  # 使用蛇形命名
            project_data = CamelCaseUtil.transform_result(project_data)  # 转换为驼峰

        prefect_data = CamelCaseUtil.transform_result(prefect_dict) if prefect_dict else {}
        opinion_data = CamelCaseUtil.transform_result(opinion_list) if opinion_list else []

        return {
            "projectInfo": project_data,
            "prefectInfo": prefect_data,
            "opinionList": opinion_data
        }

    # 4. 分页查询项目列表（按角色数据权限过滤）
    # @classmethod
    # async def get_menu_list_services(
    #     cls, query_db: AsyncSession, page_object: ProjectQueryModel, current_user: Optional[CurrentUserModel] = None
    # ) -> list[dict[str, Any]]:
    #     """
    #     获取菜单列表信息service
    #
    #     :param query_db: orm对象
    #     :param page_object: 分页查询参数对象
    #     :param current_user: 当前用户对象
    #     :return: 菜单列表信息对象
    #     """
    #     menu_list_result = await ProjectDao.get_menu_list(
    #         query_db, page_object, current_user.user.user_id, current_user.user.role
    #     )
    #
    #     return CamelCaseUtil.transform_result(menu_list_result)

    # @classmethod
    # async def import_project_by_excel_services(
    #         cls, db: AsyncSession, file_bytes: bytes, current_user: dict
    # ) -> ProjectImportResponseModel:
    #     """
    #     从Excel（陈婷芳.xlsx）批量导入项目
    #     :param file_bytes: Excel文件字节流
    #     :param current_user: 当前用户信息（项目创建人）
    #     :return: 导入结果（成功/失败数量、失败详情）
    #     """
    #     # 1. 校验角色：仅项目创建人可执行导入
    #     # if current_user["role"] != RoleConstant.PROJECT_CREATOR:
    #     #     raise ServiceException(message='仅项目创建人可执行Excel导入项目')
    #
    #     # 2. 解析Excel文件（陈婷芳.xlsx）
    #     try:
    #         # 读取Excel（使用openpyxl引擎，支持.xlsx格式）
    #         df = pd.read_excel(
    #             io=BytesIO(file_bytes),
    #             engine='openpyxl',
    #             dtype=str  # 所有字段先按字符串读取，避免数值自动转换
    #         )
    #         # 清除表头空格（如Excel表头有空格：" 项目编号 " → "项目编号"）
    #         df.columns = [col.strip() for col in df.columns]
    #         # 清除每行数据的空格
    #         df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    #         # 移除空行（所有字段都为空的行）
    #         df = df.dropna(how='all')
    #         if df.empty:
    #             return ProjectImportResponseModel(success_count=0, fail_count=0, fail_details=["Excel文件中无有效数据"])
    #     except Exception as e:
    #         raise ServiceException(message=f'Excel解析失败：{str(e)}')
    #
    #     # 3. 初始化导入结果变量
    #     success_count = 0
    #     fail_count = 0
    #     fail_details = []
    #     project_list = []  # 待批量插入的项目列表
    #     prefect_list = []  # 待批量初始化的流程列表
    #     project_codes = []  # 用于批量校验唯一性的项目编号列表
    #
    #     # 4. 逐行处理Excel数据（校验+格式转换）
    #     for row_idx, (_, row) in enumerate(df.iterrows(), start=2):  # row_idx从2开始（Excel行号：1是表头，2是第一行数据）
    #         try:
    #             # 4.1 转换Excel行数据为ExcelProjectModel（自动校验核心字段）
    #             excel_project = ExcelProjectModel(**row.to_dict())
    #             excel_project.validate_excel_fields()  # 字段非空校验
    #
    #             # 4.2 格式转换（时间、预算）
    #             excel_project.format_excel_date()  # 时间字符串→datetime
    #             excel_project.format_excel_budget()  # 预算字符串→float
    #
    #             # 4.3 校验部门存在性（通过部门名查部门ID，需部门Service支持）
    #             dept_info = await DeptService.get_dept_by_name(db, excel_project.dept_name)
    #             if not dept_info:
    #                 raise ServiceException(f'所属部门"{excel_project.dept_name}"不存在')
    #
    #             # 4.4 收集项目编号（后续批量校验唯一性）
    #             project_code = excel_project.project_code
    #             project_codes.append(project_code)
    #
    #             # 4.5 构造项目字典（适配SysProject表字段）
    #             project_dict = {
    #                 "project_code": project_code,
    #                 "project_name": excel_project.project_name,
    #                 "project_type": excel_project.project_type or "",
    #                 "dept_id": dept_info["id"],  # 部门ID（通过部门名查询得到）
    #                 "dept_name": excel_project.dept_name,
    #                 "project_manager": excel_project.project_manager or "",
    #                 "start_date": excel_project.start_date,
    #                 "end_date": excel_project.end_date,
    #                 "project_budget": excel_project.project_budget,
    #                 "project_desc": excel_project.project_desc or "",
    #                 "status": "0",  # 默认为正常状态
    #                 "create_by": current_user["user_id"],  # 导入人即创建人
    #                 "create_name": current_user["user_name"],
    #                 "create_time": pd.Timestamp.now(),
    #                 "update_by": current_user["user_id"],
    #                 "update_name": current_user["user_name"],
    #                 "update_time": pd.Timestamp.now(),
    #                 "del_flag": "0"
    #             }
    #             project_list.append(project_dict)
    #
    #         except Exception as e:
    #             # 记录失败信息（行号+原因）
    #             fail_count += 1
    #             fail_details.append(f'第{row_idx}行（项目编号：{excel_project.project_code or "未知"}）：{str(e)}')
    #
    #     # 5. 批量校验项目编号唯一性（避免重复导入）
    #     if project_codes:
    #         exist_codes = await ProjectDao.batch_get_project_by_codes(db, project_codes)
    #         if exist_codes:
    #             # 过滤掉已存在的项目
    #             filtered_project_list = []
    #             for project in project_list:
    #                 if project["project_code"] in exist_codes:
    #                     fail_count += 1
    #                     fail_details.append(f'项目编号{project["project_code"]}：已存在，导入失败')
    #                 else:
    #                     filtered_project_list.append(project)
    #             project_list = filtered_project_list  # 更新为过滤后的列表
    #
    #     # 6. 批量导入：项目+流程（事务管理）
    #     try:
    #         if project_list:
    #             # 6.1 批量插入项目
    #             await ProjectDao.batch_add_project_dao(db, project_list)
    #             # 6.2 批量查询已插入项目的ID（用于关联流程）
    #             inserted_codes = [p["project_code"] for p in project_list]
    #             inserted_projects = (
    #                 await db.execute(
    #                     select(SysProject.id, SysProject.project_code)
    #                     .where(SysProject.project_code.in_(inserted_codes), SysProject.del_flag == '0')
    #                 )
    #             ).all()
    #             # 构造项目编号→项目ID的映射
    #             code_to_id = {proj.project_code: proj.id for proj in inserted_projects}
    #
    #             # 6.3 构造批量流程列表
    #             for project in project_list:
    #                 project_id = code_to_id.get(project["project_code"])
    #                 if project_id:
    #                     prefect_dict = {
    #                         "project_id": project_id,
    #                         "current_status": PREFECT_STATUS_ENUM["CREATE"],  # 初始状态：创建人新建
    #                         "show_invoice_seal": "0",
    #                         "operator_id": current_user["user_id"],
    #                         "operator_name": current_user["user_name"],
    #                         "create_time": pd.Timestamp.now(),
    #                         "update_time": pd.Timestamp.now(),
    #                         "del_flag": "0"
    #                     }
    #                     prefect_list.append(prefect_dict)
    #
    #             # 6.4 批量初始化流程
    #             if prefect_list:
    #                 await ProjectDao.batch_init_prefect_dao(db, prefect_list)
    #
    #             # 6.5 提交事务
    #             await db.commit()
    #             success_count = len(project_list)  # 成功数量=过滤后项目列表长度
    #
    #     except Exception as e:
    #         await db.rollback()
    #         raise ServiceException(message=f'批量导入数据库失败：{str(e)}')
    #
    #     # 7. 返回导入结果
    #     return ProjectImportResponseModel(
    #         success_count=success_count,
    #         fail_count=fail_count,
    #         fail_details=fail_details
    #     )
