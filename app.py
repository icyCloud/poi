# -*- coding: utf-8 -*- 

import sys
import os

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver

from tornado.options import define, options

from mako.lookup import TemplateLookup

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from router import handlers
from config import Config, LISTEN_IP

reload(sys)
sys.setdefaultencoding('utf-8')

define("port", default=9001, help="run on the given port", type=int)

class Application(tornado.web.Application):

    def __init__(self):

        setting = dict(
            cookie_secret='you never know me',
            autoreload=True,
            gzip=True,
            login_url="/login/",
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
                
        tornado.web.Application.__init__(self, handlers, **setting)

        # templates
        self.template_lookup = TemplateLookup(
                directories=[os.path.join(os.path.dirname(__file__), 'templates')],
                module_directory=os.path.join(os.path.dirname(__file__), 'tmp/mako_modules'),
                input_encoding='utf-8',
                output_encoding='utf-8',
                default_filters=['decode.utf8'],
                encoding_errors='replace',
                )

        # db
        engine = create_engine(
                Config['db'], encoding='utf-8', echo=False,
                pool_recycle=3600
                )
        self.DB_Session = sessionmaker(bind=engine)

        engine_stock = create_engine(
                Config['db_stock'], encoding='utf-8', echo=False,
                pool_recycle=3600
                )
        self.DB_Session_stock = sessionmaker(bind=engine_stock)



def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port, address=LISTEN_IP)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
