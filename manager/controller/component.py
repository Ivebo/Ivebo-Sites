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

#Library from Google
import cloudstorage as gcs
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.api import memcache
from google.appengine.ext import blobstore
from google.appengine.api import urlfetch
import urllib

#Library System
import datetime
import cgi
import os
import sys
import logging
import urllib
import re
from django.utils import simplejson
import uuid

#Library
from manager.utils.utils import *

#Models for application
from manager.model.page import *
from manager.model.component import *

from manager.libs.sessions import *
from manager.libs.genID import *



class ComponentAdmin(BaseHandler):
    def get(self, action):
        id = GenId()
        email_admin = users.get_current_user().email()
        url_logout = users.create_logout_url("/admin")
        text_exit = {'email':email_admin,'url':url_logout}
        userID = users.get_current_user().user_id()
        apps = get_apps()
        if action == 'new':
            nav_actual = 'components'
            template_values = {
                        'exit': text_exit,
                        'nav_actual': nav_actual,
                        'id':id,
                        'apps':apps
            }
            template_name = '/manager/view/component_new.html'
            self.renderTemplate(template_name,template_values)
        if action == 'view':
            nav_actual = 'components'
            token = urllib.quote(CreateXsrfToken('delete'))
            components = Component.query(ancestor=site_key()).order(-Component.date_publication)
            template_values = {
                    'exit': text_exit,
                    'nav_actual': nav_actual,
                    'components':components,
                    'token':token,
                    'apps':apps
            }
            template_name = 'manager/view/component_view.html'
            self.renderTemplate(template_name,template_values)
        if action == 'edit':
            token = self.request.get('token')
            nav_actual = 'components'
            key = cgi.escape(self.request.get('key'))
            component = ndb.Key(urlsafe=key).get()
            template_values = {
                        'exit': text_exit,
                        'nav_actual': nav_actual,
                        'component': component,
                        'token':urllib.quote(token),
                        'apps':apps
            }
            template_name = 'manager/view/component_edit.html'
            self.renderTemplate(template_name,template_values)
        if action == 'delete':
            key = cgi.escape(self.request.get('c'))
            token = self.request.get('token')
            if ValidateXsrfToken(token,'delete'):
                component = ndb.Key(urlsafe=key).get()
                gcs.delete(component.gs_filename)
                component.key.delete()
                self.redirect('/admin/component/view')
            else:
                self.response.write('El token expiro vuelve a intentarlo <a href="/admin/component/view">Vulve a intentarlo</a>')
            
    def post(self,action):
        userID =  users.get_current_user().user_id()
        id= cgi.escape(self.request.get('id'))
        title= cgi.escape(self.request.get('title'))
        summary= cgi.escape(self.request.get('summary'))
        component_html = self.request.get('component').encode('utf-8')
        if action == 'save':
            extension_file = '.html'
            typeMIME = 'text/html'
            format = 'HTML'
            name = id+extension_file
            filename =  os.environ['bucket']+'/components/%s'%name
            gcs_file = gcs.open(filename, 'w',content_type=typeMIME)
            gcs_file.write(component_html)
            gcs_file.close()
            component = Component(
                title = title,
                title_short = title_short(title),
                idcomponent = id,
                gs_filename = filename,
                summary = summary,
                userID = userID,
                parent = site_key()
            )
            component.put()
            self.response.write(component_html)
        if action == 'update':
            key = cgi.escape(self.request.get('key'))
            component = ndb.Key(urlsafe=key).get()
            extension_file = '.html'
            typeMIME = 'text/html'
            format = 'HTML'
            filename =  component.gs_filename
            gcs_file = gcs.open(filename, 'w',content_type=typeMIME)
            gcs_file.write(component_html)
            gcs_file.close()
            component.title = title
            component.title_short = title_short(title)
            component.summary = summary
            component.userID = userID
            component.put()

class ComponentEditAdmin(BaseHandler):
    def get(self):
        key = cgi.escape(self.request.get('c'))
        try:
            component = ndb.Key(urlsafe=key).get()
            gcs_file = gcs.open(component.gs_filename)
            html_component = gcs_file.read()
            gcs_file.close()
        except:
             html_component = ''
        template_values = {
            'filecontent':'',
            'html':html_component.decode('utf-8')
        }
        template_name = '/manager/view/component_editor.html'
        self.renderTemplate(template_name,template_values)

app = webapp2.WSGIApplication([
                                RedirectRoute('/admin/component/editor',ComponentEditAdmin,name="componenteditdmin",strict_slash=True),
                                RedirectRoute('/admin/component/<action>',ComponentAdmin,name="componentdmin",strict_slash=True)
                              ],debug=debugconfig,config=confighandler)
