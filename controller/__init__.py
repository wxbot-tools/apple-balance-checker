import json
from typing import Any

import tornado.web
from tornado.escape import utf8


class BaseHandler(tornado.web.RequestHandler):

    async def options(self, *args, **kwargs):
        self.set_status(200)

    def set_default_headers(self):
        referer = self.request.headers.get('referer')
        origin = f"{referer.split(':')[0]}://{referer.split('://')[1].split('/')[0]}"
        self.set_header("Access-Control-Allow-Origin", origin)
        self.set_header("Access-Control-Allow-Credentials", 'true')
        self.set_header("Access-Control-Allow-Headers", "authorization,content-type")
        self.set_header("Access-Control-Max-Age", 3628800)
        self.set_header('Access-Control-Allow-Methods', '*')

    def data_received(self, chunk):
        pass

    def write(self, chunk) -> Any:
        if self._finished:
            raise RuntimeError("Cannot write() after finish()")
        if isinstance(chunk, (list,)):
            chunk = json.dumps(chunk, default=lambda o: o.__dict__).replace("</", "<\\/")
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            chunk = utf8(chunk)
            return self._write_buffer.append(chunk)
        super().write(chunk)
        if isinstance(chunk, bytes):
            return len(chunk)

    async def _handle(self, action):
        action = action.replace('-', '_')
        if hasattr(self, action):
            try:
                return await getattr(self, action)()
            except Exception as e:
                return self.write({
                    'error': True,
                    'message': str(e)
                })
        self.send_error(404)

    async def post(self, action):
        await self._handle(action)

    async def get(self, action):
        await self._handle(action)

    async def delete(self, action):
        await self._handle(action)


















