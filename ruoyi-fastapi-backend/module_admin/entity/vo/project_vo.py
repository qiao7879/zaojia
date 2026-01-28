from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional, Union, List
from datetime import datetime
from decimal import Decimal

from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size

from module_admin.entity.vo.project_prefect_opinion_vo import ProjectPrefectOpinionModel
from module_admin.entity.vo.project_prefect_vo import ProjectPrefectModel


# 基础模型（公共字段）
class ProjectModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    pro_id: Optional[int] = Field(default=None, description='项目ID（主键）')
    project_code: Optional[str] = Field(default=None, max_length=50, description='项目唯一编码（如XM20260101）')
    project_name: Optional[str] = Field(default=None, max_length=255, description='项目全称（Excel核心字段）')
    project_type: Optional[str] = Field(default=None, max_length=20,
                                        description='项目类型（如研发项目/运维项目，Excel字段）')

    # 业务核心字段
    ent_id: Optional[int] = Field(default=None, description='项目所属企业ID（外键→enterprise_info.ent_id）')
    ent_name: Optional[str] = Field(default=None, max_length=200, description='项目业主单位名称')
    service_content: Optional[str] = Field(default=None, max_length=100, description='项目服务内容')
    user_company: Optional[str] = Field(default=None, max_length=100, description='项目使用单位')
    project_manager: Optional[str] = Field(default=None, max_length=50, description='我方项目负责人（Excel字段）')
    coordinator: Optional[str] = Field(default=None, max_length=100, description='项目配合人员')
    contract_signed: Optional[str] = Field(default=None, max_length=20, description='合同签订状态')
    document_obtained: Optional[str] = Field(default=None, max_length=20, description='是否已取得相关文件')
    contract_amount: Optional[float] = Field(default=None, description='项目合同金额（元）')
    contract_discount: Optional[str] = Field(default=None, max_length=50, description='合同折扣说明')
    deliverable_completed: Optional[str] = Field(default=None, max_length=20, description='项目成果完成状态')
    control_price_review: Optional[str] = Field(default=None, max_length=50, description='控制价或控制价评审金额')
    settlement_submitted: Optional[float] = Field(default=0.00, description='结算送审金额（元）')
    settlement_approved: Optional[float] = Field(default=0.00, description='结算审定金额（元）')
    invoice_should_amount: Optional[float] = Field(default=None, description='项目应开具发票金额（元）')
    payment_applied: Optional[str] = Field(default=None, max_length=20, description='是否已申请付款')
    payment_month: Optional[str] = Field(default=None, max_length=20, description='请款月份')
    invoice_issued: Optional[str] = Field(default=None, max_length=20, description='是否已开具发票')
    invoice_date: Optional[datetime] = Field(default=None, description='发票开具日期')
    invoice_issued_amount: Optional[float] = Field(default=None, description='已开具发票金额（元）')
    invoice_remaining_amount: Optional[float] = Field(default=None, description='剩余可开具发票金额（元）')
    payment_received: Optional[str] = Field(default=None, max_length=20, description='业主是否已回款')
    payment_received_amount: Optional[float] = Field(default=None, description='已回款金额（元）')
    payment_received_date: Optional[datetime] = Field(default=None, description='回款到账日期')
    payment_remaining_amount: Optional[float] = Field(default=0.00, description='剩余未回款金额（元）')
    payment_recovery_rate: Optional[float] = Field(default=0.00, description='项目回款率')
    reconciliation_done: Optional[str] = Field(default=None, max_length=20, description='是否已与业主对账')
    reconciliation_date: Optional[datetime] = Field(default=None, description='双方对账日期')
    reconciliation_voucher: Optional[str] = Field(default=None, max_length=255, description='对账凭证说明或编号')
    commission_accrued: Optional[str] = Field(default=None, max_length=20, description='是否已计提提成')
    commission_amount: Optional[float] = Field(default=0.00, description='提成金额（元）')
    commission_date: Optional[datetime] = Field(default=None, description='提成计提日期')
    contract_electronic_saved: Optional[str] = Field(default=None, max_length=20, description='合同电子档是否已存档')
    contract_file: Optional[str] = Field(default=None, max_length=255, description='合同文件编号')
    deliverable_electronic_saved: Optional[str] = Field(default=None, max_length=20,
                                                        description='成果文件电子档是否已存档')
    deliverable_file: Optional[str] = Field(default=None, max_length=255, description='成果文件编号')
    document_paper_saved: Optional[str] = Field(default=None, max_length=20, description='纸质资料存档情况')
    document_save_type: Optional[str] = Field(default=None, max_length=100, description='资料存档类型说明')
    remarks: Optional[str] = Field(default=None, description='项目其他备注信息')

    # 项目时间相关字段
    start_date: Optional[datetime] = Field(default=None, description='项目开始时间（Excel字段）')
    end_date: Optional[datetime] = Field(default=None, description='项目预计结束时间（Excel字段）')
    project_budget: Optional[float] = Field(default=None, description='项目预算（Excel字段）')
    project_desc: Optional[str] = Field(default=None, description='项目描述（Excel字段）')
    status: Optional[str] = Field(default='0', max_length=1, description='项目状态（0-正常/1-暂停/2-终止）')
    prefect_status: Optional[str] = Field(default='01', max_length=255, description='项目进度状态（01-创建/02-工程师修改等）')

    # 通用字段（软删除、创建/更新信息）
    create_by: Optional[int] = Field(default=None, description='创建人ID（外键→sys_user.id，项目创建人）')
    create_name: Optional[str] = Field(default=None, max_length=30, description='创建人名称')
    create_time: Optional[datetime] = Field(default_factory=datetime.now, description='创建时间')
    update_by: Optional[int] = Field(default=None, description='更新人ID')
    update_name: Optional[str] = Field(default=None, max_length=30, description='更新人名称')
    update_time: Optional[datetime] = Field(default_factory=datetime.now, description='更新时间')
    del_flag: Optional[str] = Field(default='0', max_length=1, description='删除标志（0-存在/2-删除）')

    def validate_fields(self) -> None:
        pass


class EditProjectModel(ProjectModel):
    """修改项目请求模型（已归档前均可修改）"""
    update_by: Optional[int] = Field(default=None, description='更新人ID')
    update_name: Optional[str] = Field(default=None, description='更新人名称')


# 响应模型（项目详情/列表）
class ProjectDetailModel(BaseModel):
    """项目详情响应模型（含流程状态）"""
    project_info: Optional[ProjectModel] = Field(default=None, description='项目基础信息')
    prefect_info: Optional[ProjectPrefectModel] = Field(default=None, description='流程状态信息（当前节点、是否显示开票用章按钮）')
    opinion_list: Optional[ProjectPrefectOpinionModel] = Field(default=[], description='历史审核意见列表')


class ProjectQueryModel(ProjectModel):
    """
    企业信息不分页查询模型
    """
    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


class ProjectPageModel(ProjectQueryModel):
    """项目分页列表响应模型"""
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteProjectModel(BaseModel):
    """
    删除企业信息请求模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    pro_ids: str = Field(description='项目ID列表')


# class ExcelProjectModel(BaseModel):
#     """Excel中一行项目数据的模型（字段需与陈婷芳.xlsx表头完全对应）"""
#     model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)
#
#     # 以下字段需与陈婷芳.xlsx的表头一致（示例：假设Excel表头为"项目编号","项目名称","所属部门"等）
#     project_code: Optional[str] = Field(default=None, description='Excel表头：项目编号')
#     project_name: Optional[str] = Field(default=None, description='Excel表头：项目名称')
#     project_type: Optional[str] = Field(default=None, description='Excel表头：项目类型')
#     dept_name: Optional[str] = Field(default=None, description='Excel表头：所属部门')
#     project_manager: Optional[str] = Field(default=None, description='Excel表头：项目经理')
#     start_date: Optional[str] = Field(default=None, description='Excel表头：开始时间（格式：YYYY-MM-DD）')
#     end_date: Optional[str] = Field(default=None, description='Excel表头：预计结束时间（格式：YYYY-MM-DD）')
#     project_budget: Optional[str] = Field(default=None, description='Excel表头：项目预算（数值）')
#     project_desc: Optional[str] = Field(default=None, description='Excel表头：项目描述')
#
#     # 字段校验：核心字段非空
#
#     # @NotBlank(field_name='dept_name', message='Excel中"所属部门"字段不能为空')
#     # def validate_excel_fields(self) -> None:
#     #     """Excel字段统一校验入口"""
#     #     self.get_project_code()
#     #     self.get_project_name()
#     #     self.get_dept_name()
#
#     # 时间格式转换（Excel中字符串→datetime）
#     def format_excel_date(self) -> None:
#         """将Excel中的时间字符串（如"2026-01-01"）转换为datetime类型"""
#         if self.start_date:
#             try:
#                 self.start_date = datetime.strptime(self.start_date.strip(), "%Y-%m-%d")
#             except ValueError:
#                 raise ModelValidatorException(message=f'项目编号{self.project_code}的"开始时间"格式错误，需为YYYY-MM-DD')
#         if self.end_date and self.end_date.strip():
#             try:
#                 self.end_date = datetime.strptime(self.end_date.strip(), "%Y-%m-%d")
#             except ValueError:
#                 raise ModelValidatorException(
#                     message=f'项目编号{self.project_code}的"预计结束时间"格式错误，需为YYYY-MM-DD')
#
#     # 预算格式转换（Excel中字符串→decimal）
#     def format_excel_budget(self) -> None:
#         """将Excel中的预算字符串（如"10000.00"）转换为decimal类型"""
#         if self.project_budget and self.project_budget.strip():
#             try:
#                 self.project_budget = float(self.project_budget.strip())
#             except ValueError:
#                 raise ModelValidatorException(message=f'项目编号{self.project_code}的"项目预算"需为数值类型')
#
#
# # 导入响应模型（返回成功/失败数量、失败原因）
# class ProjectImportResponseModel(BaseModel):
#     """项目Excel导入响应模型"""
#     success_count: int = Field(default=0, description='导入成功的项目数量')
#     fail_count: int = Field(default=0, description='导入失败的项目数量')
#     fail_details: List[str] = Field(default=[], description='失败详情（如"项目编号XM001：已存在"）')
class AddProjectModel(ProjectModel):
    """新增项目请求模型"""
    @NotBlank(field_name='project_code', message='项目编号不能为空')
    @Size(field_name='project_code', max_length=30, message='项目编号长度不能超过30字符')
    def get_project_code(self) -> Union[str, None]:
        return self.project_code

    # 校验：项目名称非空
    @NotBlank(field_name='project_name', message='项目名称不能为空')
    def get_project_name(self) -> Union[str, None]:
        return self.project_name

    def validate_fields(self) -> None:
        self.get_project_code()
        self.get_project_name()
