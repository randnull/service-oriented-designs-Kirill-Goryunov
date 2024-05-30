from dao_table.user_dao import User
from common.repository.generic_repository import Repository 

user_repository = Repository[User](User)
