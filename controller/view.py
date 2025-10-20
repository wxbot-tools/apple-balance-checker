import tornado.web


class ViewHandler(tornado.web.RequestHandler):

    async def get(self, action):
        return self.render(f'{action}.html')
