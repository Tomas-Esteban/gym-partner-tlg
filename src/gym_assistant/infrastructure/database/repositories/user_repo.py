"""Repositorio de usuarios."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gym_assistant.infrastructure.database.models.user import UserModel, UserSettingModel


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_telegram_id(self, telegram_id: int) -> UserModel | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        telegram_id: int,
        username: str | None = None,
        display_name: str | None = None,
    ) -> UserModel:
        user = UserModel(
            telegram_id=telegram_id,
            username=username,
            display_name=display_name,
        )
        self._session.add(user)
        await self._session.flush()
        return user

    async def get_or_create(
        self,
        telegram_id: int,
        username: str | None = None,
        display_name: str | None = None,
    ) -> tuple[UserModel, bool]:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            return user, False
        user = await self.create(telegram_id, username, display_name)
        return user, True

    async def get_setting(self, user_id: int, key: str) -> str | None:
        result = await self._session.execute(
            select(UserSettingModel).where(
                UserSettingModel.user_id == user_id,
                UserSettingModel.key == key,
            )
        )
        setting = result.scalar_one_or_none()
        return setting.value if setting else None

    async def set_setting(self, user_id: int, key: str, value: str) -> None:
        result = await self._session.execute(
            select(UserSettingModel).where(
                UserSettingModel.user_id == user_id,
                UserSettingModel.key == key,
            )
        )
        setting = result.scalar_one_or_none()
        if setting:
            setting.value = value
        else:
            self._session.add(UserSettingModel(user_id=user_id, key=key, value=value))
        await self._session.flush()
