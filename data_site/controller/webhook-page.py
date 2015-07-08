# -*- coding: utf-8 -*-
# Copyright 2012 Ivebo.
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

#Library Google
import webapp2
from google.appengine.api import users
from google.appengine.ext import db
import jinja2
from google.appengine.api import images
from google.appengine.api import memcache
import logging

#Library System
import cgi
import os

#Libs session from manager
from manager.libs.sessions import *


class WebHookCategory(BaseHandler):
    def post(self):
        app_id = self.request.get('app_id')
        if app_id == os.environ['app_id']:
            idpage = self.request.get('idpage')
            logging.info(idpage)
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.set_status(200)
        else:
            self.abort(403)

app = webapp2.WSGIApplication([
                                RedirectRoute('/webhook-page', WebHookCategory,name="webhook-page",strict_slash=True)
                              ],debug=debugconfig,config=confighandler)

