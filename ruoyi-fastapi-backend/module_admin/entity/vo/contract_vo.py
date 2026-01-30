from datetime import date, datetime
from decimal import Decimal
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size


class ContractModel(BaseModel):
    """
    合同表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    contract_id: Optional[int] = Field(default=None, description='合同ID')
    contract_name: Optional[str] = Field(default=None, description='合同名称')
    contract_type: Optional[str] = Field(default=None, description='合同类型')
    contract_amount: Optional[Decimal] = Field(default=None, description='合同金额')
    contract_status: Optional[str] = Field(default=None, description='合同状态')
    contract_sign_date: Optional[date] = Field(default=None, description='合同签署日期')
    contract_effective_date: Optional[date] = Field(default=None, description='合同生效日期')
    contract_expire_date: Optional[date] = Field(default=None, description='合同过期日期')
    contract_terminate_date: Optional[date] = Field(default=None, description='合同终止日期')
    contract_operator: Optional[str] = Field(default=None, description='合同操作人')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    create_by: Optional[str] = Field(default=None, description='创建人')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    update_by: Optional[str] = Field(default=None, description='更新人')

    @NotBlank(field_name='contract_name', message='合同名称不能为空')
    @Size(field_name='contract_name', min_length=0, max_length=255, message='合同名称长度不能超过255个字符')
    def get_contract_name(self) -> Union[str, None]:
        return self.contract_name

    @NotBlank(field_name='contract_type', message='合同类型不能为空')
    @Size(field_name='contract_type', min_length=0, max_length=255, message='合同类型长度不能超过255个字符')
    def get_contract_type(self) -> Union[str, None]:
        return self.contract_type

    @Size(field_name='contract_status', min_length=0, max_length=255, message='合同状态长度不能超过255个字符')
    def get_contract_status(self) -> Union[str, None]:
        return self.contract_status

    @Size(field_name='contract_operator', min_length=0, max_length=255, message='合同操作人长度不能超过255个字符')
    def get_contract_operator(self) -> Union[str, None]:
        return self.contract_operator

    def validate_fields(self) -> None:
        self.get_contract_name()
        self.get_contract_type()
        self.get_contract_status()
        self.get_contract_operator()


class AddContractModel(ContractModel):
    """
    新增合同请求模型
    """


class EditContractModel(ContractModel):
    """
    修改合同请求模型
    """


class ContractPageQueryModel(ContractModel):
    """
    合同分页查询请求模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteContractModel(BaseModel):
    """
    删除合同请求模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    contract_ids: str = Field(description='合同ID列表')
