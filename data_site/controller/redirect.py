# -*- coding: utf-8 -*-
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
import webapp2
import os

DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')
if DEBUG:
    debugconfig = True
else:
    debugconfig = False

class StartHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.set_status(200)

class RedirectHandler(webapp2.RequestHandler):
	def get(self):
		if not self.request.path and not self.request.query_string:
			self.redirect(os.environ['url_site'],permanent=True)
			return
		elif self.request.path and not self.request.query_string:
			self.redirect(os.environ['url_site']+self.request.path,permanent=True)
			return
		elif self.request.path and self.request.query_string:
			self.redirect(os.environ['url_site']+self.request.path+'?'+self.request.query_string,permanent=True)
			return
		elif not self.request.path and self.request.query_string:
			self.redirect(os.environ['url_site']+'?'+self.request.query_string,permanent=True)
			return


app = webapp2.WSGIApplication([('/_ah/start',StartHandler),('/',RedirectHandler),('/.*',RedirectHandler)],debug=debugconfig,config=confighandler)