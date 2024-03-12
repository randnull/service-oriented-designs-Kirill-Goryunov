from dao_table.user_dao import User
from repository.main_repository import Repository 

user_repository = Repository[User](User)
