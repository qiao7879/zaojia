from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


# 文件上传请求模型（公共）
class FileUploadModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    business_type: str = Field(..., description='业务类型（如project_import/contract_attach）')
    business_id: Optional[str] = Field(default=None, description='关联业务ID（如项目ID/合同ID）')
    # 文件本身通过File参数传递，此处不定义


# 文件上传响应模型（公共）
class FileUploadResponseModel(BaseModel):
    file_id: Optional[int] = Field(default=None, description='文件ID')
    file_name: Optional[str] = Field(default=None, description='原始文件名')
    file_alias: Optional[str] = Field(default=None, description='存储别名')
    file_url: Optional[str] = Field(default=None, description='文件访问URL')
    file_size: Optional[int] = Field(default=None, description='文件大小（字节）')
    upload_time: Optional[str] = Field(default=None, description='上传时间')


# 批量文件上传响应模型
class BatchFileUploadResponseModel(BaseModel):
    success_count: int = Field(default=0, description='上传成功数量')
    fail_count: int = Field(default=0, description='上传失败数量')
    file_list: List[FileUploadResponseModel] = Field(default=[], description='上传成功的文件列表')
    fail_details: List[str] = Field(default=[], description='失败详情')


# 文件查询模型
class FileQueryModel(BaseModel):
    business_type: Optional[str] = Field(default=None, description='业务类型')
    business_id: Optional[str] = Field(default=None, description='关联业务ID')
    file_name: Optional[str] = Field(default=None, description='文件名模糊查询')
    page_num: int = Field(default=1, description='页码')
    page_size: int = Field(default=10, description='每页条数')
