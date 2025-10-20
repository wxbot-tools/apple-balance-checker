import asyncio
import json
import random

from loguru import logger

from model.balance_checker_account import BalanceCheckerAccount
from service import config_service
from service.balance_checker import Checker


class CheckerManager:

    def __init__(self, account: BalanceCheckerAccount):
        self._account = account
        self.checker: Checker = None
        self.version = 0
        self._available = False
        self._session_checking = False
        self._exit = False

    @property
    def country(self):
        return self._account.country

    @property
    def available(self):
        return self._available

    @property
    def account(self):
        return self._account.__dict__

    def update_account(self, account):
        self._account = account

    def exit(self):
        self._exit = True

    async def stop_checker(self):
        self._available = False
        if not self.checker:
            return
        try:
            await self.checker.stop()
            logger.warning(f'[{self._account.apple_id}]checker stopped, version: {self.version}')
        except Exception:
            logger.exception(f'[{self._account.apple_id}]stop checker failed')

    async def start_checker(self):
        self.version += 1
        version = self.version
        try:
            async with Checker(self.account) as checker:
                self.checker = checker
                if not await self.checker.login():
                    logger.warning(f'[{self._account.apple_id}]login failed')
                    return
                self._available = True
                while version == self.version:
                    await asyncio.sleep(1)
        except:
            logger.exception(f'[{self._account.apple_id}] running error')
            await self.stop_checker()

    async def check_balance(self, pin):
        try:
            if not self.available:
                return 3, None
            result = await self.checker.check(pin)
            if type(result) == str:
                result = json.loads(result)
            http_status = result['status']
            check_result = json.loads(result['body'])
            if not http_status == 200:
                return 1, None  # 会话过期了, 需要重试
            success = check_result.get('head', {}).get('status') == 200
            if success:
                return 0, check_result
            else:
                return 2, check_result
        except Exception:
            logger.exception(f'[{self._account.apple_id}] pin[{pin}] check balance error')
            return 4, None

    async def check_session(self):
        while not self._exit:
            code, _ = await self.check_balance(self._account.check_pin)
            logger.info(f'[{self._account.apple_id}]check session code: {code}')
            if not code == 0:
                await self.stop_checker()
                asyncio.create_task(self.start_checker())
            await asyncio.sleep(300)


class Manager:

    def __init__(self):
        self.accounts = []
        self.account_managers = {}

    def run(self):
        asyncio.create_task(self.start_new_accounts())

    async def start_new_accounts(self):
        while True:
            old_accounts = self.accounts
            self.accounts = await config_service.get_balance_checker_accounts(False)
            for account in self.accounts:
                account_manager = self.account_managers.get(account.apple_id)
                if not account_manager:
                    account_manager = CheckerManager(account)
                    self.account_managers[account.apple_id] = account_manager
                    asyncio.create_task(account_manager.check_session())
                else:
                    account_manager.update_account(account)
            for account in old_accounts:
                if not [a for a in self.accounts if a.apple_id == account.apple_id]:
                    account_manager = self.account_managers.get(account.apple_id)
                    if account_manager:
                        account_manager.exit()
                        await account_manager.stop_checker()
            await asyncio.sleep(60)

    def account_status(self):
        managers = list(self.account_managers.values())
        status = {}
        for manager in managers:
            status[manager._account.apple_id] = {
                'country': manager.country,
                'available': manager.available
            }
        return status

    async def check_pin(self, country, pin):
        managers = list(self.account_managers.values())
        country_managers = []
        for manager in managers:
            if not manager.available:
                continue
            if manager.country == country:
                country_managers.append(manager)
        if not country_managers:
            return {
                'success': False,
                'message': f'没有可用的余额检查会话, 地区: {country}'
            }
        code, result = await random.choice(country_managers).check_balance(pin)
        if code == 0:
            return {
                'success': True,
                'message': f'成功',
                'result': result
            }
        else:
            return {
                'success': False,
                'message': f'余额检查失败, 错误代码: {code}, 地区: {country}'
            }


