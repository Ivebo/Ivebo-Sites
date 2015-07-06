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

#Library from Google
import cloudstorage as gcs
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import images
from google.appengine.ext import blobstore

#Library System
import datetime
import cgi
import os
import uuid

#Library
from manager.utils.utils import *

from manager.libs.sessions import *


class Image(BaseHandler):
    def get(self):
        template_values = {
                       
        } 
        template_name = '/manager/view/files_image.html'
        self.renderTemplate(template_name,template_values)
    def post(self):
        upload_files = self.request.POST['imgpage']
        userID =  users.get_current_user().user_id()
        if len(str(upload_files)) > 0:
            try:
                image = images.Image(image_data=upload_files.value)
            except: 
                self.response.write('No es una imagen valida')
                return
            if image.format == images.JPEG:
                extension_file = '.jpg'
                typeMIME = 'image/jpeg'
                format = 'JPEG'
            elif image.format == images.PNG:
                extension_file = '.png'
                typeMIME = 'image/png'
                format = 'PNG'
            elif image.format == images.GIF:
                extension_file = '.gif'
                typeMIME = 'image/gif'
                format = 'GIF'
            else:
                self.response.write('La imagen no tiene un formato válido')
                return
            name = str(uuid.uuid4().int)+extension_file
            filename = os.environ['bucket']+'/pages/%s'%name
            gcs_file = gcs.open(filename, 'w',content_type=typeMIME)
            gcs_file.write(upload_files.value)
            gcs_file.close()
            blobstore_filename = '/gs' + filename
            gs_key = blobstore.create_gs_key(blobstore_filename)
            url = images.get_serving_url(gs_key,secure_url=True,size=0)
            template_values = {
                'fileurl' : url
            } 
            template_name = '/manager/view/files_upload_image.html'
            self.renderTemplate(template_name,template_values)
        else:
            self.response.write('Escoge una imagen para insertar <a href="/admin/files/image">Volver</a>')

app = webapp2.WSGIApplication([
                                RedirectRoute('/admin/files/image',Image,name="filesadmin",strict_slash=True)
                              ],debug=debugconfig,config=confighandler)
