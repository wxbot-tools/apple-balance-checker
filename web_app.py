import tornado.escape
import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import config
from controller.balance import BalanceHandler, start_manager
from controller.config import ConfigHandler
from controller.view import ViewHandler

urls = [
    (r"/config/(.+)", ConfigHandler),
    (r"/balance/(.+)", BalanceHandler),
    (r"/view/(.+)", ViewHandler),
]
configs = {
    'debug': False,
    'compress_response': True,
    'template_path': 'views',
    'compiled_template_cache': False,
    'static_path': 'statics',
    'websocket_ping_interval': 9,
    'websocket_ping_timeout': 20
}


class CCApplication(tornado.web.Application):

    def __init__(self, urls, configs):
        super(CCApplication, self).__init__(handlers=urls, **configs)


def make_app():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(CCApplication(urls, configs), xheaders=True)
    tornado.ioloop.IOLoop.configure("tornado.platform.asyncio.AsyncIOLoop")
    io_loop = tornado.ioloop.IOLoop.current()
    http_server.listen(config.port)
    io_loop.run_sync(start_manager)
    io_loop.start()


# 启动服务器
if __name__ == '__main__':
    make_app()
