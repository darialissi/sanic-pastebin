from .repository import UsersRepository
from .service import UsersService

user_service: UsersService = UsersService(users_repo=UsersRepository)
