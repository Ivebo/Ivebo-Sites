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

#Library System
import datetime
import cgi
import os
import sys
import re

#Models for application
import model.page

from config.config import *
from config.configown import *


class ListCategory(webapp2.RequestHandler):
    def get(self,category):
        pages = model.page.CategoryList(category,'all')
        title = title_site + ' - '+category
        template_values = {
                'pages':pages,
                'title':title
        }
        path = os.path.join(os.curdir, '..','view','list.html')  
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([
                                RedirectRoute('/list/<category>', ListCategory,name="listcategory",strict_slash=True)
                              ],debug=debugconfig)

