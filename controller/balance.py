import json
import platform

from controller import BaseHandler

from service.balance_checker_manager import Manager

manager = Manager()


async def start_manager():
    if platform.system().lower() == 'windows':
        manager.run()


class BalanceHandler(BaseHandler):

    async def checker_status(self):
        self.write(manager.account_status())

    async def check(self):
        data = json.loads(self.request.body)
        country = data['country']
        pin = data['pin']
        result = await manager.check_pin(country, pin)
        self.write(result or {})
