# -*- coding: utf-8 
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from manager.utils.utils import *
import webapp2
import jinja2
import logging
import os

from webapp2_extras import sessions
from webapp2_extras.routes import RedirectRoute
from webapp2_extras.routes import DomainRoute

DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')
if DEBUG:
    debugconfig = True
else:
    debugconfig = False


confighandler = {
  'webapp2_extras.sessions': {
    'secret_key': os.environ['secret_key_sessions'],'cookie_name':os.environ['cookie_name_sessions']
  }
}


class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def printMessage(self,message,urlcontinue=None):
        #Error pagina no encontrada
        if message == '404':
            self.error('404')
            logging.info(u'[404] Se intentó acceder a una página que no existe')
            template_values = {
                'mensaje': u'Nuestros robots no encontraron la página que buscas, ya los estamos reprogramando o talvez te equivocaste en escribir la dirección vuelve a intentarlo.',
                'site': os.environ['SERVER_NAME']
            }
            jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.abspath('.')))
            template = jinja_environment.get_template('manager/view/error.html')
            self.response.out.write(template.render(template_values))

    def renderTemplate(self,template_name,template_vars):
        jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.abspath('.')))
        template = jinja_environment.get_template(template_name)
        self.response.out.write(template.render(template_vars))

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

