from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional, Union, List
from datetime import datetime

from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size


# 基础模型（公共字段）
class ProjectModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='项目ID')
    project_code: Optional[str] = Field(default=None, description='项目编号')
    project_name: Optional[str] = Field(default=None, description='项目名称')
    project_type: Optional[str] = Field(default=None, description='项目类型')
    dept_id: Optional[int] = Field(default=None, description='所属部门ID')
    dept_name: Optional[str] = Field(default=None, description='所属部门名称')
    project_manager: Optional[str] = Field(default=None, description='项目经理')
    start_date: Optional[datetime] = Field(default=None, description='项目开始时间')
    end_date: Optional[datetime] = Field(default=None, description='项目预计结束时间')
    project_budget: Optional[float] = Field(default=None, description='项目预算')
    project_desc: Optional[str] = Field(default=None, description='项目描述')
    create_by: Optional[int] = Field(default=None, description='创建人ID（项目创建人）')
    create_name: Optional[str] = Field(default=None, description='创建人名称')

    # 校验：项目编号非空且唯一（业务层进一步校验）
    @NotBlank(field_name='project_code', message='项目编号不能为空')
    @Size(field_name='project_code', max_length=30, message='项目编号长度不能超过30字符')
    def get_project_code(self) -> Union[str, None]:
        return self.project_code

    # 校验：项目名称非空
    @NotBlank(field_name='project_name', message='项目名称不能为空')
    def get_project_name(self) -> Union[str, None]:
        return self.project_name


# 请求模型（新增/修改项目）
class AddProjectModel(ProjectModel):
    """项目创建人新建项目请求模型"""
    pass


class EditProjectModel(ProjectModel):
    """修改项目请求模型（已归档前均可修改）"""
    update_by: Optional[int] = Field(default=None, description='更新人ID')
    update_name: Optional[str] = Field(default=None, description='更新人名称')


# 响应模型（项目详情/列表）
class ProjectDetailModel(BaseModel):
    """项目详情响应模型（含流程状态）"""
    project_info: Optional[ProjectModel] = Field(default=None, description='项目基础信息')
    prefect_info: Optional[dict] = Field(default=None, description='流程状态信息（当前节点、是否显示开票用章按钮）')
    opinion_list: Optional[List[dict]] = Field(default=[], description='历史审核意见列表')


class ProjectPageModel(BaseModel):
    """项目分页列表响应模型"""
    total: Optional[int] = Field(default=0, description='总条数')
    rows: List[Union[ProjectModel, None]] = Field(default=[], description='项目列表')


class ExcelProjectModel(BaseModel):
    """Excel中一行项目数据的模型（字段需与陈婷芳.xlsx表头完全对应）"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    # 以下字段需与陈婷芳.xlsx的表头一致（示例：假设Excel表头为"项目编号","项目名称","所属部门"等）
    project_code: Optional[str] = Field(default=None, description='Excel表头：项目编号')
    project_name: Optional[str] = Field(default=None, description='Excel表头：项目名称')
    project_type: Optional[str] = Field(default=None, description='Excel表头：项目类型')
    dept_name: Optional[str] = Field(default=None, description='Excel表头：所属部门')
    project_manager: Optional[str] = Field(default=None, description='Excel表头：项目经理')
    start_date: Optional[str] = Field(default=None, description='Excel表头：开始时间（格式：YYYY-MM-DD）')
    end_date: Optional[str] = Field(default=None, description='Excel表头：预计结束时间（格式：YYYY-MM-DD）')
    project_budget: Optional[str] = Field(default=None, description='Excel表头：项目预算（数值）')
    project_desc: Optional[str] = Field(default=None, description='Excel表头：项目描述')

    # 字段校验：核心字段非空
    @NotBlank(field_name='project_code', message='Excel中"项目编号"字段不能为空')
    @NotBlank(field_name='project_name', message='Excel中"项目名称"字段不能为空')
    @NotBlank(field_name='dept_name', message='Excel中"所属部门"字段不能为空')
    def validate_excel_fields(self) -> None:
        """Excel字段统一校验入口"""
        self.get_project_code()
        self.get_project_name()
        self.get_dept_name()

    # 时间格式转换（Excel中字符串→datetime）
    def format_excel_date(self) -> None:
        """将Excel中的时间字符串（如"2026-01-01"）转换为datetime类型"""
        if self.start_date:
            try:
                self.start_date = datetime.strptime(self.start_date.strip(), "%Y-%m-%d")
            except ValueError:
                raise ModelValidatorException(message=f'项目编号{self.project_code}的"开始时间"格式错误，需为YYYY-MM-DD')
        if self.end_date and self.end_date.strip():
            try:
                self.end_date = datetime.strptime(self.end_date.strip(), "%Y-%m-%d")
            except ValueError:
                raise ModelValidatorException(
                    message=f'项目编号{self.project_code}的"预计结束时间"格式错误，需为YYYY-MM-DD')

    # 预算格式转换（Excel中字符串→decimal）
    def format_excel_budget(self) -> None:
        """将Excel中的预算字符串（如"10000.00"）转换为decimal类型"""
        if self.project_budget and self.project_budget.strip():
            try:
                self.project_budget = float(self.project_budget.strip())
            except ValueError:
                raise ModelValidatorException(message=f'项目编号{self.project_code}的"项目预算"需为数值类型')


# 导入响应模型（返回成功/失败数量、失败原因）
class ProjectImportResponseModel(BaseModel):
    """项目Excel导入响应模型"""
    success_count: int = Field(default=0, description='导入成功的项目数量')
    fail_count: int = Field(default=0, description='导入失败的项目数量')
    fail_details: List[str] = Field(default=[], description='失败详情（如"项目编号XM001：已存在"）')
