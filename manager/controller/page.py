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

from manager.libs.sessions import *



class PageAdmin(BaseHandler):
    def get(self, action):
        email_admin = users.get_current_user().email()
        url_logout = users.create_logout_url("/admin")
        text_exit = {'email':email_admin,'url':url_logout}
        userID = users.get_current_user().user_id()
        if action == 'new':
            nav_actual = 'pages'
            template_values = {
                        'exit': text_exit,
                        'nav_actual': nav_actual
            }
            template_name = '/manager/view/pages_new.html'
            self.renderTemplate(template_name,template_values)
        if action == 'view':
            viewpages = cgi.escape(self.request.get('view'))
            if not viewpages:
                categories_array = []
                category = PageCategory.query(ancestor=site_key()).filter(PageCategory.category_parent == None).order(PageCategory.name)
                for c in category:
                    if c.name_short != 'empty':
                        categories_array.append({'name':c.name,'key':c.key.urlsafe(),'idcategory':c.idcategory,'date_publication':c.date_publication})
                nav_actual = 'pages'
                cat_empty = PageCategory.query(PageCategory.name_short == 'empty').get()
                pages_in_catgegory = PagesinCategory.query(ancestor=site_key()).filter(PagesinCategory.category == cat_empty.key).order(-PagesinCategory.date_publication)
                pages =[]
                for p in pages_in_catgegory:
                    page = p.page.get()
                    pages.append({'title':page.title,'key':page.key.urlsafe(),'idpage':page.idpage,'date_publication':page.date_publication})
                token = urllib.quote(CreateXsrfToken('delete'))
                template_values = {
                        'category': categories_array,
                        'exit': text_exit,
                        'nav_actual': nav_actual,
                        'view':'home',
                        'catactual':'Inicio',
                        'pages':pages,
                        'token':token
                }
                template_name = 'manager/view/pages_view.html'
                self.renderTemplate(template_name,template_values)
                return
            if viewpages == 'category':
                keycategory = cgi.escape(self.request.get('key'))
                key = ndb.Key(urlsafe=keycategory)
                viewcategory = key.get()
                categories_array = []
                category = PageCategory.query(ancestor=site_key()).filter(PageCategory.category_parent == viewcategory.key).order(PageCategory.name)
                for c in category:
                    if c.name_short != 'empty':
                        categories_array.append({'name':c.name,'key':c.key.urlsafe(),'idcategory':c.idcategory,'date_publication':c.date_publication})
                pages_in_catgegory = PagesinCategory.query(ancestor=site_key()).filter(PagesinCategory.category == viewcategory.key).order(-PagesinCategory.date_publication)
                pages =[]
                for p in pages_in_catgegory:
                    page = p.page.get()
                    pages.append({'title':page.title,'key':page.key.urlsafe(),'idpage':page.idpage,'date_publication':page.date_publication})
                nav_actual = 'pages'
                try:
                    parentcategory = viewcategory.category_parent
                    catactual = '<a href="/admin/page/view">Inicio</a> > <a href="/admin/page/view?key=%s&view=category">%s</a> > %s '%(parentcategory.key(),parentcategory.name,viewcategory.name)
                except:
                    catactual = '<a href="/admin/page/view">Inicio</a> > '+viewcategory.name
                token = urllib.quote(CreateXsrfToken('delete'))
                template_values = {
                        'category': categories_array,
                        'pages':pages,
                        'exit': text_exit,
                        'nav_actual': nav_actual,
                        'view':'category',
                        'catactual':viewcategory.name,
                        'token':token
                }
                template_name = 'manager/view/pages_view.html'
                self.renderTemplate(template_name,template_values)
                return
        if action == 'edit':
            token = self.request.get('token')
            nav_actual = 'pages'
            html = ''
            page_key = cgi.escape(self.request.get('key'))
            page = ndb.Key(urlsafe=page_key)
            page = page.get()
            categories = PagesinCategory.query(ancestor=site_key()).filter(PagesinCategory.page == page.key).order(-PagesinCategory.date_publication)
            htmlcategories = ''
            responsegroups = {}
            categoiresnames = []
            for c in categories:
                category = c.category.get()
                if category.name_short != 'empty':
                    htmlcategories += '<a href="#%s" class="categorybtn">%s</a>'%(category.key.id(),category.name)
                    categoiresnames.append({'catid':category.key.id(),'catname':category.name})
            responsegroups.update({'groups':categoiresnames})
            categoryarray = simplejson.dumps(responsegroups)
            template_values = {
                        'categories': htmlcategories,
                        'categoriesnames': categoryarray,
                        'exit': text_exit,
                        'nav_actual': nav_actual,
                        'page': page,
                        'key': page_key,
                        'token':urllib.quote(token)
            }
            template_name = 'manager/view/pages_edit.html'
            self.renderTemplate(template_name,template_values)
        if action == 'delete':
            page_key = cgi.escape(self.request.get('page'))
            token = self.request.get('token')
            if ValidateXsrfToken(token,'delete'):
                page_key = ndb.Key(urlsafe=page_key)
                page = page_key.get()
                page_in_category = PagesinCategory.query(PagesinCategory.page == page.key).get()
                if page.gs_key and page.gs_filename:
                    # blobstore.delete(page.gs_key)
                    images.delete_serving_url(page.gs_key)
                    gcs.delete(page.gs_filename)
                page.key.delete()
                page_in_category.key.delete()
                self.redirect('/admin/page/new')
            else:
                self.redirect('/admin/page/view')
            
    def post(self,action):
        userID =  users.get_current_user().user_id()
        title = cgi.escape(self.request.get('titlepage'))
        summary = cgi.escape(self.request.get('summarypage')[:500])
        categories = cgi.escape(self.request.get('categories'))
        upload_files = self.request.POST['imgpage']
        content = self.request.get('contentpage')
        featured = cgi.escape(self.request.get('featured'))
        parent = site_key()
        if action == 'save':
            featured = True if featured == 'yes' else False
            if len(str(upload_files)) > 0:
                try:
                    image = images.Image(image_data=upload_files.value)
                except: 
                    self.response.write('No es una imagen valida')
                    return
                try: 
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
                except: 
                    self.response.write('No es una imagen valida')
                    return
                name = str(uuid.uuid4().int)+extension_file
                filename =  os.environ['bucket']+'/pages/%s'%name
                gcs_file = gcs.open(filename, 'w',content_type=typeMIME)
                gcs_file.write(upload_files.value)
                gcs_file.close()
                blobstore_filename = '/gs' + filename
                gs_key = blobstore.create_gs_key(blobstore_filename)
                url = images.get_serving_url(gs_key,secure_url=True,size=0)
                idpage = GenId()
                page = Page(
                    title = title,
                    title_short = title_short(title),
                    idpage = idpage,
                    image_url = url,
                    gs_key = gs_key,
                    gs_filename = filename,
                    content = content,
                    date_publication = datetime.datetime.utcnow()-datetime.timedelta(hours=5),
                    summary= summary,
                    featured = featured,
                    userID = userID,
                    parent= parent
                    )
                page_model = page.put()
                page_model = page_model.get()
                if page_model:
                    if categories:
                        categories = categories.split(',')
                        for c in categories:
                            cat = c.split('/')[0]
                            cat = PageCategory.get_by_id(int(cat),parent=site_key())
                            page_in_category = PagesinCategory(
                                page = page_model.key,
                                category = cat.key,
                                date_publication = datetime.datetime.utcnow(),
                                parent = site_key()
                                )
                            page_in_category.put()
                        self.redirect('/admin/page/new') 
                        
                    else:
                        category_empty = PageCategory.get_or_insert(
                            'empty',
                            name = validstringName('Empty'),
                            name_short = 'empty',
                            idcategory = GenId(),
                            date_publication = datetime.datetime.utcnow(),
                            userID = users.get_current_user().user_id(),
                            category_parent = None,
                            parent = site_key(),
                            )
                        page_in_category = PagesinCategory(
                            page = page_model.key,
                            category = category_empty.key,
                            date_publication = datetime.datetime.utcnow(),
                            parent = site_key()
                            )
                        page_in_category.put()
                        self.redirect('/admin/page/new')
            else:
                idpage = GenId()
                page = Page(
                    title = title,
                    title_short = title_short(title),
                    idpage = idpage,
                    image_url = None,
                    gs_key = None,
                    gs_filename = None,
                    content = content,
                    date_publication = datetime.datetime.utcnow(),
                    summary= summary,
                    featured = featured,
                    userID = userID,
                    parent = parent
                    )
                page_model = page.put()
                page_model = page_model.get()
                if page_model:
                    if categories:
                        categories = categories.split(',')
                        for c in categories:
                            cat = c.split('/')[0]
                            cat = PageCategory.get_by_id(int(cat),parent=site_key())
                            page_in_category = PagesinCategory(
                                page = page_model.key,
                                category = cat.key,
                                date_publication = datetime.datetime.utcnow(),
                                parent = site_key()
                                )
                            page_in_category.put()
                        self.redirect('/admin/page/new') 
                    else:
                        category_empty = PageCategory.get_or_insert(
                            'empty',
                            name = validstringName('Empty'),
                            name_short = 'empty',
                            idcategory = GenId(),
                            date_publication = datetime.datetime.utcnow(),
                            userID = users.get_current_user().user_id(),
                            category_parent = None,
                            parent = site_key(),
                            )
                        page_in_category = PagesinCategory(
                            page = page_model.key,
                            category = category_empty.key,
                            date_publication = datetime.datetime.utcnow(),
                            parent = site_key()
                            )
                        page_in_category.put()
                        self.redirect('/admin/page/new')

        if action == 'update':
            page_key = cgi.escape(self.request.get('key'))
            page_key = ndb.Key(urlsafe=page_key)
            page = page_key.get()
            featured = True if featured == 'yes' else False
            if len(str(upload_files)) > 0:
                try:
                    image = images.Image(image_data=upload_files.value)
                except: 
                    self.response.write('No es una imagen valida')
                    return
                try: 
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
                except: 
                    self.response.write('No es una imagen valida')
                    return
                name = str(uuid.uuid4().int)+extension_file
                filename =  os.environ['bucket']+'/pages/%s'%name
                gcs_file = gcs.open(filename, 'w',content_type=typeMIME)
                gcs_file.write(upload_files.value)
                gcs_file.close()
                blobstore_filename = '/gs' + filename
                gs_key = blobstore.create_gs_key(blobstore_filename)
                url = images.get_serving_url(gs_key,secure_url=True,size=0)
                idpage = GenId()
                page.title = title
                page.title_short = title_short(title)
                page.image_url = url
                page.gs_key = gs_key
                page.gs_filename = filename
                page.content = content
                page.summary= summary
                page.featured = featured
                page.userID = userID
                page_model = page.put()
                page_model = page_model.get()
                if page_model:
                    page_in_category = PagesinCategory.query(ancestor=site_key()).filter(PagesinCategory.page == page_model.key)
                    for p in page_in_category:
                        p.key.delete()
                    if categories:
                        categories = categories.split(',')
                        for c in categories:
                            cat = c.split('/')[0]
                            cat = PageCategory.get_by_id(int(cat),parent=site_key())
                            page_in_category = PagesinCategory(
                                page = page_model.key,
                                category = cat.key,
                                date_publication = datetime.datetime.utcnow(),
                                parent = site_key()
                                )
                            page_in_category.put()
                        self.redirect('/admin/page/view') 
                    else:
                        category_empty = PageCategory.get_or_insert(
                            'empty',
                            name = validstringName('Empty'),
                            name_short = 'empty',
                            idcategory = GenId(),
                            date_publication = datetime.datetime.utcnow(),
                            userID = users.get_current_user().user_id(),
                            category_parent = None,
                            parent = site_key(),
                            )
                        page_in_category = PagesinCategory(
                            page = page_model.key,
                            category = category_empty.key,
                            date_publication = datetime.datetime.utcnow(),
                            parent = site_key()
                            )
                        page_in_category.put()
                        self.redirect('/admin/page/view')
            else:
                page.title = title
                page.title_short = title_short(title)
                if not page.image_url:
                    page.image_url = None
                    page.gs_key = None
                    page.gs_filename = None
                page.content = content
                page.summary= summary
                page.featured = featured
                page.userID = userID
                page_model = page.put()
                page_model = page_model.get()
                if page_model:
                    page_in_category = PagesinCategory.query(ancestor=site_key()).filter(PagesinCategory.page == page_model.key)
                    for p in page_in_category:
                        p.key.delete()
                    if categories:
                        categories = categories.split(',')
                        for c in categories:
                            cat = c.split('/')[0]
                            cat = PageCategory.get_by_id(int(cat),parent=site_key())
                            page_in_category = PagesinCategory(
                                page = page_model.key,
                                category = cat.key,
                                date_publication = datetime.datetime.utcnow(),
                                parent = site_key()
                                )
                            page_in_category.put()
                        self.redirect('/admin/page/view') 
                    else:
                        category_empty = PageCategory.get_or_insert(
                            'empty',
                            name = validstringName('Empty'),
                            name_short = 'empty',
                            idcategory = GenId(),
                            date_publication = datetime.datetime.utcnow(),
                            userID = users.get_current_user().user_id(),
                            category_parent = None,
                            parent = site_key(),
                            )
                        page_in_category = PagesinCategory(
                            page = page_model.key,
                            category = category_empty.key,
                            date_publication = datetime.datetime.utcnow(),
                            parent = site_key()
                            )
                        page_in_category.put()
                        self.redirect('/admin/page/view')


app = webapp2.WSGIApplication([
                                RedirectRoute('/admin/page/<action>',PageAdmin,name="pageadmin",strict_slash=True)
                              ],debug=debugconfig,config=confighandler)
