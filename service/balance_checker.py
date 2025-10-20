import asyncio
import json
import platform
import random
import traceback

import aiofiles
from loguru import logger

import config
from service import config_service

if platform.system().lower() == 'windows':
    from playwright.async_api import async_playwright, ViewportSize, Page, Route, \
        TimeoutError as _TimeoutError, Error, ProxySettings, BrowserContext, Response, APIRequestContext, Playwright


class Checker:

    def __init__(self, account):
        self.apple_id = account['apple_id']
        self.password = account['password']
        self.country = account['country']
        region = self.country.lower()
        if region == 'us':
            region = ''
        elif region == 'gb':
            region = '/uk'
        else:
            region = f'/{region}'
        self.region = region
        self.initialized = False
        self.playwright = None
        self.browser = None
        self.context = None
        self.page: Page = None
        self.params = {
            'scnt': None,
            'login_complete': None,
            'auth_success': None,
            'x-aos-stk': '',
            'x-as-actk': '',
        }

    async def __aenter__(self):
        try:
            playwright_context = async_playwright()
            self.playwright = await playwright_context.start()
            if not platform.system().lower() == 'windows':
                proxy = None
            else:
                proxy = await config_service.get_proxy(self.country)
            self.browser = await self.playwright.chromium.launch(
                channel='chrome',
                args=['--disable-infobars', '--disable-sync', '--bwsi', '--no-sandbox',
                      '--start-maximized', '--disable-extensions', '--disable-java',
                      '--disable-pinch', '--allow-insecure-websocket-from-https-origin',
                      '--disable-web-security',
                      '--proxy-server=direct://',
                      '--proxy-bypass-list=*',
                      '--disable-blink-features', '--disable-blink-features=AutomationControlled',
                      '--disable-software-rasterizer',
                      '--disable-features=PreloadMediaEngagementData, MediaEngagementBypassAutoplayPolicies',
                      '--ignore-certificate-errors', '--enable-quic', '--disable-client-side-phishing-detection',
                      "--ignore-ssl-errors",
                      '--safebrowsing-disable-download-protection', '--allow-running-insecure-content',
                      # '--disable-extensions-except={}'.format(os.path.join(exec_dir, 'extensions', 'Helper')),
                      # '--load-extensions={}'.format(os.path.join(exec_dir, 'extensions', 'Helper')),
                      '--safebrowsing-disable-auto-update'],
                handle_sigint=False,
                handle_sigterm=False,
                handle_sighup=False,
                headless=False,
                proxy=proxy
            )
            self.context: BrowserContext = await self.browser.new_context(
                viewport=None,
                no_viewport=True,
                ignore_https_errors=True,
                java_script_enabled=True,
                bypass_csp=True,
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                accept_downloads=False,
                proxy=proxy
            )
            self.page = await self.context.new_page()
            self.page.set_default_timeout(0)
            await self.page.goto(f"https://secure6.store.apple.com{self.region}/shop/giftcard/balance")
            await self.page.wait_for_load_state('networkidle')
            await self.page.wait_for_load_state('domcontentloaded')
            await self.page.wait_for_selector('iframe')
            self.initialized = True
        except:
            logger.exception('initial browser error')
        return self

    async def __aexit__(
        self,
        exc_type=None,
        exc_value=None,
        exc_tb=None,
    ) -> None:
        if exc_type:
            traceback.print_exception(exc_type, exc_value, exc_tb)
        await self.stop()

    async def stop(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        await self.playwright.stop()

    async def login(self):
        if not self.initialized:
            return False

        async def monitor_request(response: Response):
            url = response.url
            if url == 'https://idmsa.apple.com/appleauth/auth/federate?isRememberMeEnabled=true':
                self.params['scnt'] = await response.header_value('scnt')
            elif url == 'https://idmsa.apple.com/appleauth/auth/signin/complete?isRememberMeEnabled=true':
                if not response.ok:
                    self.params['auth_success'] = False
                else:
                    data = await response.json()
                    if data['authType'] == 'sa' and list(filter(lambda o: 'myacinfo' in o, await response.header_values('set-cookie'))):
                        self.params['login_complete'] = True
                    else:
                        self.params['login_complete'] = False
            elif f'{self.region}/shop/signIn/idms/authx?ssi=' in url:
                if not response.ok:
                    self.params['auth_success'] = False
                else:
                    # logger.info(f'[{self.apple_id}]authx response: {text}')
                    self.params['x-aos-stk'] = await response.request.header_value('x-aos-stk')
                    self.params['auth_success'] = True
            elif url.endswith(f'{self.region}/shop/giftcard/balance'):
                try:
                    text = await response.text()
                    self.params['x-as-actk'] = text.split('"x-as-actk":"')[1].split('"')[0]
                except:
                    pass

        self.page.on("response", monitor_request)

        frame = self.page.frame('aid-auth-widget')
        await frame.wait_for_load_state('networkidle')
        await frame.wait_for_load_state('domcontentloaded')
        await frame.wait_for_selector('#account_name_text_field')
        await frame.fill('#account_name_text_field', self.apple_id)
        await frame.focus('#account_name_text_field')
        await frame.wait_for_selector('#sign-in')
        await frame.click('#sign-in')
        await frame.wait_for_load_state('networkidle')
        await frame.wait_for_load_state('domcontentloaded')

        await frame.wait_for_selector('#password_text_field')
        await frame.fill('#password_text_field', self.password)
        await frame.focus('#password_text_field')
        await frame.click('#sign-in')

        await frame.wait_for_load_state('networkidle')
        await frame.wait_for_load_state('domcontentloaded')

        while True:
            if self.params['login_complete'] is not None and not self.params['login_complete']:
                logger.info(f'[{self.apple_id}]login failed')
                return False
            if self.params['auth_success'] is not None and not self.params['auth_success']:
                logger.info(f'[{self.apple_id}]authx failed')
                return False
            if self.params['auth_success']:
                break
            await asyncio.sleep(1)
        await self.page.wait_for_function("""() => {
            return !!document.getElementById('giftCardBalanceCheck.giftCardPin');
        }""")
        return True

    async def check(self, pin):
        return await self.page.evaluate("""async ([pin1, pin2, pin3, pin4, x_aos_stk, x_as_actk, region]) => {
            const res = await fetch(`${region}/shop/giftcard/balancex?_a=checkBalance&_m=giftCardBalanceCheck`, {
                method: 'POST',
                headers: {
                    "content-type": "application/x-www-form-urlencoded",
                    "modelversion": "v2",
                    "syntax": "graviton",
                    "x-aos-model-page": 'giftCardBalancePage',
                    'x-aos-stk': x_aos_stk,
                    'x-as-actk': x_as_actk,
                    'x-aos-ui-fetch-call-1': Math.random().toString(36).substring(2, 12) + "-" + Date.now().toString(36),
                    'x-requested-with': 'Fetch',
                },
                body: `giftCardBalanceCheck.giftCardPin=${pin1}%20${pin2}%20${pin3}%20${pin4}&giftCardBalanceCheck.deviceID=%7B%22op%22%3A%22DEVICEID%22%7D`
            });
            return {status: res.status, body: await res.text()};
        }""", [pin[0:4], pin[4:8], pin[8:12], pin[12:], self.params['x-aos-stk'], self.params['x-as-actk'], self.region])



