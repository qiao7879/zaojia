from typing import Any, Optional

from sqlalchemy import and_, desc, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_admin.entity.do.file_do import FILE_STATUS_ENUM, SysFile
from module_admin.entity.vo.file_vo import FileQueryModel
from utils.page_util import PageUtil


class FileDao:
    """通用文件DAO层"""

    # 1. 新增文件记录
    @classmethod
    async def add_file_dao(cls, db: AsyncSession, file_info: dict[str, Any]) -> SysFile:
        db_file = SysFile(**file_info)
        db.add(db_file)
        await db.flush()
        return db_file

    # 2. 批量新增文件记录
    @classmethod
    async def batch_add_file_dao(cls, db: AsyncSession, file_list: list[dict[str, Any]]) -> None:
        if not file_list:
            return
        await db.execute(insert(SysFile), file_list)

    # 3. 按ID查询文件
    @classmethod
    async def get_file_by_id(cls, db: AsyncSession, file_id: int) -> Optional[SysFile]:
        result = (
            (
                await db.execute(
                    select(SysFile).where(
                        and_(
                            SysFile.id == file_id, SysFile.del_flag == '0', SysFile.status == FILE_STATUS_ENUM['NORMAL']
                        )
                    )
                )
            )
            .scalars()
            .first()
        )
        return result

    # 4. 按业务类型+业务ID查询文件
    @classmethod
    async def get_files_by_business(cls, db: AsyncSession, business_type: str, business_id: str) -> list[SysFile]:
        result = (
            (
                await db.execute(
                    select(SysFile)
                    .where(
                        and_(
                            SysFile.business_type == business_type,
                            SysFile.business_id == business_id,
                            SysFile.del_flag == '0',
                            SysFile.status == FILE_STATUS_ENUM['NORMAL'],
                        )
                    )
                    .order_by(desc(SysFile.create_time))
                )
            )
            .scalars()
            .all()
        )
        return result

    # 5. 分页查询文件
    @classmethod
    async def get_file_page_dao(cls, db: AsyncSession, query_params: FileQueryModel) -> PageModel:
        query = (
            select(SysFile)
            .where(
                and_(
                    SysFile.del_flag == '0',
                    SysFile.status == FILE_STATUS_ENUM['NORMAL'],
                    SysFile.business_type == query_params.business_type if query_params.business_type else True,
                    SysFile.business_id == query_params.business_id if query_params.business_id else True,
                    SysFile.file_name.like(f'%{query_params.file_name}%') if query_params.file_name else True,
                )
            )
            .order_by(desc(SysFile.create_time))
        )
        page_result = await PageUtil.paginate(db, query, query_params.page_num, query_params.page_size)
        return page_result

    # 6. 软删除文件（修改状态）
    @classmethod
    async def delete_file_dao(cls, db: AsyncSession, file_id: int, update_user_id: int) -> None:
        await db.execute(
            update(SysFile)
            .where(SysFile.id == file_id)
            .values(status=FILE_STATUS_ENUM['DELETE'], update_time=func.now(), update_by=update_user_id)
        )
