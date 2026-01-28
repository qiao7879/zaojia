from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size


class EnterpriseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    ent_id: Optional[int] = Field(default=None, description='主键ID')
    enterprise_name: Optional[str] = Field(default=None, description='企业名称')
    taxpayer_id: Optional[str] = Field(default=None, description='纳税人识别号')
    ent_type: Optional[int] = Field(default=None, description='企业类型')
    address: Optional[str] = Field(default=None, description='企业地址')
    contact_person: Optional[str] = Field(default=None, description='联系人')
    contact_phone: Optional[str] = Field(default=None, description='联系电话')
    bank_name: Optional[str] = Field(default=None, description='开户行')
    bank_account: Optional[str] = Field(default=None, description='银行账号')
    create_by: Optional[str] = Field(default=None, description='创建人')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新人')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='enterprise_name', message='企业名称不能为空')
    @Size(field_name='enterprise_name', min_length=0, max_length=200, message='企业名称长度不能超过200个字符')
    def get_enterprise_name(self) -> Union[str, None]:
        return self.enterprise_name

    @NotBlank(field_name='taxpayer_id', message='纳税人识别号不能为空')
    @Size(field_name='taxpayer_id', min_length=0, max_length=20, message='纳税人识别号长度不能超过20个字符')
    def get_taxpayer_id(self) -> Union[str, None]:
        return self.taxpayer_id

    @NotBlank(field_name='ent_type', message='企业类型不能为空')
    def get_ent_type(self) -> Union[int, None]:
        return self.ent_type

    @Size(field_name='address', min_length=0, max_length=500, message='企业地址长度不能超过500个字符')
    def get_address(self) -> Union[str, None]:
        return self.address

    @Size(field_name='contact_person', min_length=0, max_length=50, message='联系人长度不能超过50个字符')
    def get_contact_person(self) -> Union[str, None]:
        return self.contact_person

    @Size(field_name='contact_phone', min_length=0, max_length=20, message='联系电话长度不能超过20个字符')
    def get_contact_phone(self) -> Union[str, None]:
        return self.contact_phone

    @Size(field_name='bank_name', min_length=0, max_length=100, message='开户行长度不能超过255个字符')
    def get_bank_name(self) -> Union[str, None]:
        return self.bank_name

    @Size(field_name='bank_account', min_length=0, max_length=30, message='银行账号长度不能超过30个字符')
    def get_bank_account(self) -> Union[str, None]:
        return self.bank_account

    def validate_fields(self) -> None:
        self.get_enterprise_name()
        self.get_taxpayer_id()
        self.get_ent_type()
        self.get_address()
        self.get_contact_person()
        self.get_contact_phone()
        self.get_bank_name()
        self.get_bank_account()


class AddEnterpriseModel(EnterpriseModel):
    """
    添加企业信息请求模型
    """

    pass


class EditEnterpriseModel(EnterpriseModel):
    """
    修改企业信息请求模型
    """

    update_by: Optional[str] = Field(None, description='更新人')
    update_time: Optional[str] = Field(None, description='更新时间')


class EnterpriseDetailModel(BaseModel):
    """
    企业信息详情响应模型
    """
    enterprise_info: Optional[EnterpriseModel] = Field(None, description='企业信息')


class EnterprisePageModel(EnterpriseModel):
    """
    企业信息分页响应模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class EnterpriseQueryModel(EnterpriseModel):
    """
    企业信息不分页查询模型
    """

    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


class DeleteEnterpriseModel(BaseModel):
    """
    删除企业信息请求模型
    """
    model_config = ConfigDict(alias_generator=to_camel)
    ent_ids: str = Field(description='企业ID列表')
