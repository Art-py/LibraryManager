from fastapi import Depends

from repositories.users.uow import UserUOW


class UserService:
    def __init__(self, unit: UserUOW = Depends(UserUOW)):
        self.unit = unit

    async def create_user(self):
        pass
