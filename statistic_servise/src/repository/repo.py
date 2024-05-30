from dao_table.dao import Statistic
from common.repository.generic_repository import Repository 

statistic_repository = Repository[Statistic](Statistic)
