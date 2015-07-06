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

#Library System
import datetime
import cgi
import os
import sys
import re

#Models for Manager
from manager.model.page import *

#Libs session from manager
from manager.libs.sessions import *

class PageIndexHandler(BaseHandler):
    def get(self):
        title_site = os.environ['title_site']
        template_values = {
            'title_site':title_site,
            'description':'Home'
        }
        template_name = 'data_site/view/index.html'
        self.renderTemplate(template_name,template_values)


class PageHandler(BaseHandler):
    def get(self,page):
        page = Page.query(Page.title_short == page).get()
        if page:
            title_site = os.environ['title_site']=':'+page.title
            template_values = {
                'page':page,
                'title_site':title_site,
                'description':page.summary
            }
            template_name = 'data_site/view/page.html'
            self.renderTemplate(template_name,template_values)
        else:
            self.printMessage('404')


app = webapp2.WSGIApplication([
                                RedirectRoute('/',PageIndexHandler,name="index",strict_slash=True),
                                RedirectRoute('/<page>',PageHandler,name="page",strict_slash=True)
                              ],debug=debugconfig,config=confighandler)

