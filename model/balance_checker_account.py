
from model import BaseModel


class BalanceCheckerAccount(BaseModel):

    def __init__(self, apple_id, password, country, check_pin):
        self.attr_setter(self, **locals())

    @classmethod
    def empty_instance(cls):
        return BalanceCheckerAccount(None, None, None, None)

