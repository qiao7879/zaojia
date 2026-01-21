from io import BytesIO

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, List, Dict, Any

from common.vo import CrudResponseModel
from exceptions.exception import ServiceException
from module_admin.dao.project_dao import ProjectDao
from module_admin.dao.project_prefect_dao import ProjectPrefectDao
from module_admin.dao.project_prefect_opinion_dao import ProjectPrefectOpinionDao
from module_admin.entity.do.project_do import SysProject
from module_admin.entity.do.project_prefect_do import PREFECT_STATUS_ENUM
from module_admin.entity.vo.project_vo import AddProjectModel, EditProjectModel, ProjectImportResponseModel, \
    ExcelProjectModel
from module_admin.service.dept_service import DeptService


# from app.modules.project.dao.project_dao import ProjectDao
# from app.modules.project.dao.project_prefect_dao import ProjectPrefectDao
# from app.modules.project.dao.project_prefect_opinion_dao import ProjectPrefectOpinionDao
# from app.modules.project.model.project_vo import AddProjectModel, EditProjectModel, ProjectDetailModel
# from app.modules.project.model.project_prefect_do import PREFECT_STATUS_ENUM
# from app.common.model.crud_response_model import CrudResponseModel
# from app.common.exception.service_exception import ServiceException
# from app.common.constant.role_constant import RoleConstant  # 新增角色常量


class ProjectService:
    """项目主表业务逻辑层"""

    # 1. 项目创建人新建项目（同步初始化流程）
    @classmethod
    async def add_project_services(
            cls, db: AsyncSession, project: AddProjectModel, current_user: dict
    ) -> CrudResponseModel:
        try:
            # 校验：项目创建人角色
            # if current_user["role"] != RoleConstant.PROJECT_CREATOR:
            #     raise ServiceException(message='仅项目创建人可新建项目')

            # 校验：项目编号唯一
            exist_project = await ProjectDao.get_project_by_id(db, project.project_code)
            if exist_project:
                raise ServiceException(message=f'项目编号{project.project_code}已存在')

            # 补充创建人信息
            project.create_by = current_user["user_id"]
            project.create_name = current_user["user_name"]

            # 1. 新增项目主表
            db_project = await ProjectDao.add_project_dao(db, project)

            # 2. 同步初始化流程（状态：项目创建人新建）
            prefect_data = {
                "project_id": db_project.id,
                "current_status": PREFECT_STATUS_ENUM["CREATE"],
                "show_invoice_seal": '0',
                "operator_id": current_user["user_id"],
                "operator_name": current_user["user_name"]
            }
            await ProjectPrefectDao.init_prefect_dao(db, prefect_data)

            await db.commit()
            return CrudResponseModel(is_success=True, message='项目新建成功', data={"project_id": db_project.id})
        except Exception as e:
            await db.rollback()
            raise e

    # 2. 修改项目（已归档前均可修改）
    @classmethod
    async def edit_project_services(
            cls, db: AsyncSession, project: EditProjectModel, current_user: dict
    ) -> CrudResponseModel:
        try:
            # 校验：项目是否存在
            exist_project = await ProjectDao.get_project_by_id(db, project.id)
            if not exist_project:
                raise ServiceException(message=f'项目ID{project.id}不存在')

            # 校验：项目是否已归档（已归档不可修改）
            prefect_info = await ProjectPrefectDao.get_prefect_by_project_id(db, project.id)
            if prefect_info and prefect_info.current_status == PREFECT_STATUS_ENUM["ARCHIVED"]:
                raise ServiceException(message='项目已归档，不可修改')

            # 校验：角色权限（项目创建人/工程师/项目成员可修改）
            # allow_roles = [RoleConstant.PROJECT_CREATOR, RoleConstant.ENGINEER, RoleConstant.PROJECT_MEMBER]
            # if current_user["role"] not in allow_roles:
            #     raise ServiceException(message='仅项目创建人、工程师、项目成员可修改项目')

            # 补充更新人信息
            project.update_by = current_user["user_id"]
            project.update_name = current_user["user_name"]

            # 执行修改
            await ProjectDao.edit_project_dao(db, project)
            await db.commit()
            return CrudResponseModel(is_success=True, message='项目修改成功')
        except Exception as e:
            await db.rollback()
            raise e

    # 3. 查询项目详情（含流程状态、历史意见）
    @classmethod
    async def get_project_detail_services(cls, db: AsyncSession, project_id: int) -> Dict[str, Any]:
        # 1. 查询项目基础信息
        project_info = await ProjectDao.get_project_by_id(db, project_id)
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

        return {
            "project_info": project_info.__dict__,
            "prefect_info": prefect_dict,
            "opinion_list": opinion_list
        }

    # 4. 分页查询项目列表（按角色数据权限过滤）
    @classmethod
    async def get_project_page_services(
            cls, db: AsyncSession, query_params: dict, data_scope_sql: Any, current_user: dict
    ) -> Dict[str, Any]:
        # 执行分页查询
        project_page = await ProjectDao.get_project_page_dao(db, query_params, data_scope_sql)
        return project_page.__dict__ if hasattr(project_page, '__dict__') else project_page

    @classmethod
    async def import_project_by_excel_services(
            cls, db: AsyncSession, file_bytes: bytes, current_user: dict
    ) -> ProjectImportResponseModel:
        """
        从Excel（陈婷芳.xlsx）批量导入项目
        :param file_bytes: Excel文件字节流
        :param current_user: 当前用户信息（项目创建人）
        :return: 导入结果（成功/失败数量、失败详情）
        """
        # 1. 校验角色：仅项目创建人可执行导入
        # if current_user["role"] != RoleConstant.PROJECT_CREATOR:
        #     raise ServiceException(message='仅项目创建人可执行Excel导入项目')

        # 2. 解析Excel文件（陈婷芳.xlsx）
        try:
            # 读取Excel（使用openpyxl引擎，支持.xlsx格式）
            df = pd.read_excel(
                io=BytesIO(file_bytes),
                engine='openpyxl',
                dtype=str  # 所有字段先按字符串读取，避免数值自动转换
            )
            # 清除表头空格（如Excel表头有空格：" 项目编号 " → "项目编号"）
            df.columns = [col.strip() for col in df.columns]
            # 清除每行数据的空格
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            # 移除空行（所有字段都为空的行）
            df = df.dropna(how='all')
            if df.empty:
                return ProjectImportResponseModel(success_count=0, fail_count=0, fail_details=["Excel文件中无有效数据"])
        except Exception as e:
            raise ServiceException(message=f'Excel解析失败：{str(e)}')

        # 3. 初始化导入结果变量
        success_count = 0
        fail_count = 0
        fail_details = []
        project_list = []  # 待批量插入的项目列表
        prefect_list = []  # 待批量初始化的流程列表
        project_codes = []  # 用于批量校验唯一性的项目编号列表

        # 4. 逐行处理Excel数据（校验+格式转换）
        for row_idx, (_, row) in enumerate(df.iterrows(), start=2):  # row_idx从2开始（Excel行号：1是表头，2是第一行数据）
            try:
                # 4.1 转换Excel行数据为ExcelProjectModel（自动校验核心字段）
                excel_project = ExcelProjectModel(**row.to_dict())
                excel_project.validate_excel_fields()  # 字段非空校验

                # 4.2 格式转换（时间、预算）
                excel_project.format_excel_date()  # 时间字符串→datetime
                excel_project.format_excel_budget()  # 预算字符串→float

                # 4.3 校验部门存在性（通过部门名查部门ID，需部门Service支持）
                dept_info = await DeptService.get_dept_by_name(db, excel_project.dept_name)
                if not dept_info:
                    raise ServiceException(f'所属部门"{excel_project.dept_name}"不存在')

                # 4.4 收集项目编号（后续批量校验唯一性）
                project_code = excel_project.project_code
                project_codes.append(project_code)

                # 4.5 构造项目字典（适配SysProject表字段）
                project_dict = {
                    "project_code": project_code,
                    "project_name": excel_project.project_name,
                    "project_type": excel_project.project_type or "",
                    "dept_id": dept_info["id"],  # 部门ID（通过部门名查询得到）
                    "dept_name": excel_project.dept_name,
                    "project_manager": excel_project.project_manager or "",
                    "start_date": excel_project.start_date,
                    "end_date": excel_project.end_date,
                    "project_budget": excel_project.project_budget,
                    "project_desc": excel_project.project_desc or "",
                    "status": "0",  # 默认为正常状态
                    "create_by": current_user["user_id"],  # 导入人即创建人
                    "create_name": current_user["user_name"],
                    "create_time": pd.Timestamp.now(),
                    "update_by": current_user["user_id"],
                    "update_name": current_user["user_name"],
                    "update_time": pd.Timestamp.now(),
                    "del_flag": "0"
                }
                project_list.append(project_dict)

            except Exception as e:
                # 记录失败信息（行号+原因）
                fail_count += 1
                fail_details.append(f'第{row_idx}行（项目编号：{excel_project.project_code or "未知"}）：{str(e)}')

        # 5. 批量校验项目编号唯一性（避免重复导入）
        if project_codes:
            exist_codes = await ProjectDao.batch_get_project_by_codes(db, project_codes)
            if exist_codes:
                # 过滤掉已存在的项目
                filtered_project_list = []
                for project in project_list:
                    if project["project_code"] in exist_codes:
                        fail_count += 1
                        fail_details.append(f'项目编号{project["project_code"]}：已存在，导入失败')
                    else:
                        filtered_project_list.append(project)
                project_list = filtered_project_list  # 更新为过滤后的列表

        # 6. 批量导入：项目+流程（事务管理）
        try:
            if project_list:
                # 6.1 批量插入项目
                await ProjectDao.batch_add_project_dao(db, project_list)
                # 6.2 批量查询已插入项目的ID（用于关联流程）
                inserted_codes = [p["project_code"] for p in project_list]
                inserted_projects = (
                    await db.execute(
                        select(SysProject.id, SysProject.project_code)
                        .where(SysProject.project_code.in_(inserted_codes), SysProject.del_flag == '0')
                    )
                ).all()
                # 构造项目编号→项目ID的映射
                code_to_id = {proj.project_code: proj.id for proj in inserted_projects}

                # 6.3 构造批量流程列表
                for project in project_list:
                    project_id = code_to_id.get(project["project_code"])
                    if project_id:
                        prefect_dict = {
                            "project_id": project_id,
                            "current_status": PREFECT_STATUS_ENUM["CREATE"],  # 初始状态：创建人新建
                            "show_invoice_seal": "0",
                            "operator_id": current_user["user_id"],
                            "operator_name": current_user["user_name"],
                            "create_time": pd.Timestamp.now(),
                            "update_time": pd.Timestamp.now(),
                            "del_flag": "0"
                        }
                        prefect_list.append(prefect_dict)

                # 6.4 批量初始化流程
                if prefect_list:
                    await ProjectDao.batch_init_prefect_dao(db, prefect_list)

                # 6.5 提交事务
                await db.commit()
                success_count = len(project_list)  # 成功数量=过滤后项目列表长度

        except Exception as e:
            await db.rollback()
            raise ServiceException(message=f'批量导入数据库失败：{str(e)}')

        # 7. 返回导入结果
        return ProjectImportResponseModel(
            success_count=success_count,
            fail_count=fail_count,
            fail_details=fail_details
        )
