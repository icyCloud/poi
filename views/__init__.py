# -*- coding: utf-8 -*-

import sys
import logging


from tornado.web import RequestHandler, HTTPError
from mako import exceptions


class BaseHandler(RequestHandler):

    def initialize(self):
        #self.db = self.application.DB_Session()
        self.db = self.application.db_session

    def on_finish(self):
        #self.db.close()
        pass

    def render(self, template_name, **kwargs):
        lookup = self.application.template_lookup

        env_kwargs = dict(
            handler=self,
            request=self.request,
            locale=self.locale,
            _=self.locale.translate,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.application.reverse_url,
        )
        env_kwargs.update(kwargs)

        try:
            template = lookup.get_template(template_name)
            self.finish(template.render(**env_kwargs))
        except:
            self.finish(exceptions.html_error_template().render())

    #def _handle_request_exception(self, e):
        #self.db.rollback()
        #self.log_exception(sys.exc_info())
        #if self._finished:
            #return
        #logging(e)
        #self.finish()
