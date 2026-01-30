from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank

from exceptions.exception import ModelValidatorException
from module_admin.entity.do.project_prefect_do import PREFECT_STATUS_ENUM


# 基础模型
class ProjectPrefectModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='流程ID')
    pro_id: Optional[int] = Field(default=None, description='项目ID')
    current_status: Optional[str] = Field(default=None, description='当前流程状态')
    show_invoice_seal: Optional[str] = Field(default='0', description='是否显示开票/用章按钮（0-不显示/1-显示）')
    operator_id: Optional[int] = Field(default=None, description='操作人ID')
    operator_name: Optional[str] = Field(default=None, description='操作人名称')
    create_time: Optional[datetime] = Field(default_factory=datetime.now, description='创建时间')
    update_time: Optional[datetime] = Field(default_factory=datetime.now, description='更新时间')
    del_flag: Optional[str] = Field(default='0', max_length=1, description='删除标志（0-存在/2-删除）')

    # 校验：项目ID非空
    @NotBlank(field_name='pro_id', message='项目ID不能为空')
    def get_project_id(self) -> Union[int, None]:
        return self.pro_id


# 请求模型（更新流程状态）
class UpdatePrefectStatusModel(ProjectPrefectModel):
    """更新流程状态请求模型（如创建人下发工程师、复审通过/驳回）"""

    target_status: Optional[str] = Field(default=None, description='目标状态')
    opinion_content: Optional[str] = Field(default=None, description='当前节点审核意见（必填）')

    # 校验：目标状态合法
    @model_validator(mode='after')
    def check_target_status(self) -> 'UpdatePrefectStatusModel':
        valid_status = list(PREFECT_STATUS_ENUM.values())
        if self.target_status not in valid_status:
            raise ModelValidatorException(message=f'目标状态不合法，合法状态：{valid_status}')
        return self

    # 校验：审核意见非空（复审节点必填）
    @model_validator(mode='after')
    def check_opinion(self) -> 'UpdatePrefectStatusModel':
        review_status = [PREFECT_STATUS_ENUM['SECOND_REVIEW'], PREFECT_STATUS_ENUM['THIRD_REVIEW']]
        if self.current_status in review_status and (
            not self.opinion_content or len(self.opinion_content.strip()) == 0
        ):
            raise ModelValidatorException(message='复审节点必须填写审核意见')
        return self


class BatchUpdatePrefectStatusModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    pro_ids: list[int] = Field(description='项目ID列表')
    current_status: str = Field(description='当前流程状态')
    target_status: str = Field(description='目标状态')
    opinion_content: Optional[str] = Field(default=None, description='当前节点审核意见（必填）')

    @model_validator(mode='after')
    def check_pro_ids(self) -> 'BatchUpdatePrefectStatusModel':
        if not self.pro_ids or not isinstance(self.pro_ids, list):
            raise ModelValidatorException(message='项目ID列表不能为空')
        invalid_ids = [i for i in self.pro_ids if not isinstance(i, int) or i <= 0]
        if invalid_ids:
            raise ModelValidatorException(message=f'项目ID列表存在非法值：{invalid_ids}')
        return self

    @model_validator(mode='after')
    def check_status(self) -> 'BatchUpdatePrefectStatusModel':
        valid_status = list(PREFECT_STATUS_ENUM.values())
        if self.current_status not in valid_status:
            raise ModelValidatorException(message=f'当前状态不合法，合法状态：{valid_status}')
        if self.target_status not in valid_status:
            raise ModelValidatorException(message=f'目标状态不合法，合法状态：{valid_status}')
        return self

    @model_validator(mode='after')
    def check_opinion(self) -> 'BatchUpdatePrefectStatusModel':
        review_status = [PREFECT_STATUS_ENUM['SECOND_REVIEW'], PREFECT_STATUS_ENUM['THIRD_REVIEW']]
        if self.current_status in review_status and (
            not self.opinion_content or len(self.opinion_content.strip()) == 0
        ):
            raise ModelValidatorException(message='复审节点必须填写审核意见')
        return self


# 响应模型（流程详情）
class PrefectDetailModel(BaseModel):
    """流程详情响应模型"""

    data: Optional[ProjectPrefectModel] = Field(default=None, description='流程基础信息')
    opinion_list: Optional[list[dict]] = Field(default=[], description='该流程的所有审核意见')
