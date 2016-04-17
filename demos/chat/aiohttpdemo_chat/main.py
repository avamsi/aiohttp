import asyncio
import jinja2
import logging

from aiohttp import web
import aiohttp_jinja2

from aiohttpdemo_chat.views import setup as setup_routes


async def init(loop):
    app = web.Application(loop=loop)
    app['sockets'] = []
    app.on_shutdown.append(shutdown)

    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('aiohttpdemo_chat', 'templates'))

    setup_routes(app)

    return app


async def shutdown(app):
    for ws in app['sockets']:
        await ws.close()
    app['sockets'].clear()


def main():
    # init logging
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init(loop))
    web.run_app(app)


if __name__ == '__main__':
    main()