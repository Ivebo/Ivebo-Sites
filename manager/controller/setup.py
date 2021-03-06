﻿# -*- coding: utf-8 -*-
# Copyright 2015 Ivebo.
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
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import logging
from manager.libs.sessions import *
from manager.model.page import *
import datetime

class SetupHandler(BaseHandler):
    def get(self):
    	category_empty = PageCategory(
    	    name = validstringName('Empty'),
    	    name_short = 'empty',
    	    idcategory = GenId(),
    	    date_publication = datetime.datetime.utcnow(),
    	    userID = users.get_current_user().user_id(),
    	    category_parent = None,
    	    parent = site_key(),
    	    id='empty'
    	    )
    	category_empty.put()
       	self.response.write('Instalacion completa')
   
    

app = webapp2.WSGIApplication([
                                RedirectRoute('/admin/setup',SetupHandler,name="setup",strict_slash=True)
                              ],debug=debugconfig,config=confighandler)
