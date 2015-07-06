# -*- coding: utf-8 -*-
#Library from Google
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import images

#Library System
import datetime
import cgi
import os
import sys
import logging
import urllib
import re
import sys


#Library
from manager.utils.utils import *

#Models for application
from manager.model.page import *

from manager.libs.sessions import *

def CategoryRootExist(category_short):
    categories = PageCategory.query(PageCategory.category_parent == None, PageCategory.name_short == category_short).get()
    if categories:
        return True
    else:
        return False

def CategoryChildExist(category_parent,category_short):
    catparentid = category_parent.key.id()
    categories = PageCategory.query(PageCategory.name_short == category_short)
    if categories:
        for c in categories:
            if not c.category_parent == None:
                if catparentid == c.category_parent.id():
                    return True 
                else:
                    return False
    else:
      return False


class CategoryView(BaseHandler):
    def get(self):
        email = users.get_current_user().email()
        userID = users.get_current_user().user_id()
        categories_array = []
        categories = PageCategory.query(ancestor=site_key()).filter(PageCategory.category_parent == None).order(PageCategory.name_short)
        for c in categories:
            if c.name_short != 'empty':
                subcategories = PageCategory.query(PageCategory.category_parent == c.key)
                categories_array.append({'category':c,'subcategories':subcategories})
        template_values = {
                'titlepopup': 'Categorias',
                'categories': categories_array
        }
        template_name = '/manager/view/categorypopup.html'
        self.renderTemplate(template_name,template_values)

class CategoryEdit(BaseHandler):
    def get(self):
        key = cgi.escape(self.request.get('key'))
        if not key:
            categories = model.page.PageCategory.all()
            categories.filter('category_parent =', None)
            categories.order('name_short')
            totalcategories = categories.count()
            categories = categories.fetch(totalcategories)
            template_values = {
                    'titlepopup': 'Categorias',
                    'categories': categories
            }
            path = os.path.join(os.curdir, '..', '..','view','admin','categorypopup_view.html')  
            self.response.out.write(template.render(path, template_values))
            return
        category = model.page.PageCategory.get(key)
        template_values = {
                'titlepopup': 'Categorias',
                'category': category
        }
        template_name = '/view/admin/categorypopup_edit.html'
        self.renderTemplate(template_name,template_values)

    def post(self):
        name = cgi.escape(self.request.get('category'))
        summary = cgi.escape(self.request.get('summary'))
        key = cgi.escape(self.request.get('key'))
        catexist = model.page.CategoryExist(name)
        if catexist:
            category = model.page.PageCategory.get(key)
            category.summary = summary
            category.put()
            self.response.out.write(u'<p>Guardado el resumen <a href="/admin/category/edit">Regresar</a> </p>')
            return
        category = model.page.PageCategory.get(key)
        category.name = validstringName(name)
        category_valida  = model.page.namecategory_short(name)
        category.name_short = category_valida
        category.summary = summary
        category.put()
        self.response.out.write(u'<p>Guardado <a href="/admin/category/edit">Regresar</a> </p>')

        
                
class CategoryPost(BaseHandler):
    def post(self, action):
        email = users.get_current_user().email()
        userID = users.get_current_user().user_id()
        if action == 'add':
            category = cgi.escape(self.request.get('category'))
            parent = cgi.escape(self.request.get('categories'))
            parentbool = cgi.escape(self.request.get('parentbool'))
            if category:
                if not parentbool == 'parent':
                    category_valida  = short_text(category)
                    boolCatExist = CategoryRootExist(category_valida)
                    if boolCatExist:
                        self.response.write('La categoría existe <a href="/admin/category/view">Volver</a>')
                    else:
                        idcategory = GenId()
                        category = PageCategory(
                            name = validstringName(category),
                            name_short = category_valida,
                            idcategory = idcategory,
                            date_publication = datetime.datetime.utcnow(),
                            userID = users.get_current_user().user_id(),
                            category_parent = None,
                            parent = site_key()
                            )
                        category.put()
                        self.redirect('/admin/category/view')
                else:
                    if not parent:
                        self.response.write('No existen categorías padres creadas <a href="/admin/category/view">Volver</a>')
                        return
                    categoryparent = PageCategory.get_by_id(int(parent),parent=site_key())
                    category_valida  = short_text(category)
                    boolCatExist = CategoryChildExist(categoryparent,category_valida)
                    if boolCatExist:
                        self.response.out.write('La categoría existe <a href="/admin/category/view">Volver</a>')
                    else:
                        idcategory = GenId()
                        category = PageCategory(
                            name = validstringName(category),
                            name_short = category_valida,
                            idcategory = idcategory,
                            date_publication = datetime.datetime.utcnow(),
                            userID = users.get_current_user().user_id(),
                            category_parent = categoryparent.key,
                            parent = site_key(),
                            )
                        category.put()
                        self.redirect('/admin/category/view')
            else:
                self.response.write('Error ingresando la categoría <a href="/admin/category/view">Volver</a>')
   

app = webapp2.WSGIApplication([
                                RedirectRoute('/admin/category/view',CategoryView,name="categoryviewadmin",strict_slash=True),
                                RedirectRoute('/admin/category/edit',CategoryEdit,name="categoryeditadmin",strict_slash=True),
                                RedirectRoute('/admin/category/<action>',CategoryPost,name="categorypostdmin",strict_slash=True)
                              ],debug=debugconfig,config=confighandler)