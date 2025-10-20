import json

from controller import BaseHandler
from service import config_service


class ConfigHandler(BaseHandler):

    async def proxy(self):
        if self.request.method.lower() == 'post':
            await config_service.set_proxy(json.loads(self.request.body))
            return self.write({})
        elif self.request.method.lower() == 'get':
            return self.write(await config_service.get_proxy())
    
    async def check_proxy(self):
        if self.request.method.lower() == 'post':
            return self.write(await config_service.check_proxy(json.loads(self.request.body)))

    async def balance_check_account(self):
        if self.request.method.lower() == 'post':
            await config_service.add_balance_check_account(json.loads(self.request.body))
            return self.write({})
        elif self.request.method.lower() == 'get':
            return self.write(await config_service.get_balance_checker_accounts())
        elif self.request.method.lower() == 'delete':
            await config_service.del_balance_check_account(self.get_argument('apple_id'))
            return self.write({})



