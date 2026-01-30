from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


# 基础模型
class ProjectPrefectOpinionModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='意见ID')
    project_id: Optional[int] = Field(default=None, description='项目ID')
    prefect_id: Optional[int] = Field(default=None, description='流程ID')
    node_code: Optional[str] = Field(default=None, description='节点编码')
    node_name: Optional[str] = Field(default=None, description='节点名称')

    opinion_content: Optional[str] = Field(default=None, description='审核意见')

    operator_id: Optional[int] = Field(default=None, description='操作人ID')
    operator_name: Optional[str] = Field(default=None, description='操作人名称')
    operator_role: Optional[str] = Field(default=None, description='操作人角色')
    create_time: Optional[datetime] = Field(default=None, description='填写时间')


# 请求模型（新增意见）
class AddPrefectOpinionModel(ProjectPrefectOpinionModel):
    """新增审核意见请求模型"""

    # 校验：核心字段非空
    # @NotBlank(field_name='node_code', message='节点编码不能为空')
    # @NotBlank(field_name='operator_role', message='操作人角色不能为空')
    # def validate_core_fields(self) -> None:
    #     pass


# 响应模型（意见列表）
class OpinionListModel(BaseModel):
    """审核意见列表响应模型"""

    total: Optional[int] = Field(default=0, description='总条数')
    rows: list[Union[ProjectPrefectOpinionModel, None]] = Field(default=[], description='意见列表')
