import json

import aiofiles
import httpx
import random

import config
from model.balance_checker_account import BalanceCheckerAccount


async def get_balance_checker_accounts(raw=True):
    async with aiofiles.open(config.balance_checker_accounts_file, "r", encoding='utf-8') as f:
        accounts = json.loads(await f.read())
        if raw:
            return accounts
        return [
            BalanceCheckerAccount(**a)
            for a in accounts
        ]


async def get_proxy(country: str) -> dict:
    async with aiofiles.open(config.proxy_config_file, "r", encoding='utf-8') as f:
        data = json.loads(await f.read())
        server = data.get('server')
        username = data.get('username')
        password = data.get('password')
        provider = data['provider']
        if provider == '922proxy':
            return {
                'server': server,
                'username': f'{username}-{country.upper()}-sessid-{str(random.randint(10000, 1000000))}-sessTime-5',
                'password': password,
            }
        else:
            raise ValueError('不支持的代理服务商')


async def check_proxy(data):
    server = data.get('server')
    username = data.get('username')
    password = data.get('password')
    provider = data['provider']
    if provider == '922proxy':
        if not username or not password:
            raise ValueError('用户名和密码为必填项')
        proxy = f'http://{username}-US-sessid-{str(random.randint(10000, 1000000))}-sessTime-5:G6xwpnyc@{server}'
    else:
        raise ValueError('不支持的代理服务商')

    async with httpx.AsyncClient(proxy=proxy) as client:
        response = await client.get('http://ipinfo.io/json')
        return response.json()


async def set_proxy(data):
    async with aiofiles.open(config.proxy_config_file, "w", encoding='utf-8') as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=4))


async def add_balance_check_account(data):
    accounts = await get_balance_checker_accounts()
    accounts.append(data)
    async with aiofiles.open(config.balance_checker_accounts_file, "w", encoding='utf-8') as f:
        await f.write(json.dumps(accounts, ensure_ascii=False, indent=4))


async def del_balance_check_account(apple_id):
    accounts = await get_balance_checker_accounts()
    accounts = [a for a in accounts if not a['apple_id'] == apple_id]
    async with aiofiles.open(config.balance_checker_accounts_file, "w", encoding='utf-8') as f:
        await f.write(json.dumps(accounts, ensure_ascii=False, indent=4))



