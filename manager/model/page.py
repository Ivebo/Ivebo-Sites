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
from google.appengine.ext import ndb
from google.appengine.api import search

#Library
from manager.utils.utils import *
from manager.utils.genID import PushID

import os

INDEX_PAGES = 'pages'

class PageCategory(ndb.Model):
    name = ndb.StringProperty(required=True)
    name_short = ndb.StringProperty(required=True)
    category_parent = ndb.KeyProperty(kind='PageCategory')
    summary = ndb.StringProperty()
    idcategory = ndb.StringProperty(required=True)
    image_url = ndb.StringProperty()
    date_publication = ndb.DateTimeProperty()
    date_updated = ndb.DateTimeProperty(auto_now_add=True)
    userID = ndb.StringProperty(required=True)
    language = ndb.StringProperty(default='es')
    
class Page(ndb.Model):
    title = ndb.StringProperty(required=True)
    title_short = ndb.StringProperty(required=True)
    idpage = ndb.StringProperty(required=True)
    image_url = ndb.StringProperty()
    gs_key = ndb.StringProperty()
    gs_filename = ndb.StringProperty()
    content = ndb.TextProperty()
    summary = ndb.StringProperty()
    order = ndb.IntegerProperty()
    date_publication = ndb.DateTimeProperty()
    date_updated = ndb.DateTimeProperty(auto_now_add=True)
    userID = ndb.StringProperty(required=True)
    visibility = ndb.StringProperty(choices=set(['public','private']),required=True,default='public')
    status = ndb.StringProperty(choices=set(['published','unpublished','archived','trashed']),required=True,default='published')
    featured = ndb.BooleanProperty(default=False)
    language = ndb.StringProperty(default='es')

class PagesinCategory(ndb.Model):
    page = ndb.KeyProperty(kind=Page)
    category = ndb.KeyProperty(kind=PageCategory)
    date_publication = ndb.DateTimeProperty()
    date_updated = ndb.DateTimeProperty(auto_now_add=True)


def title_short(string):
    string = short_text(string)
    return string

def GenId():
    p = PushID()
    p = p.next_id()
    return p

def site_key():
  return ndb.Key('Site', os.environ['site'])

def IndexPages(title, idpage, summary, content):
    return search.Document(
        doc_id = idpage,
        fields=[search.TextField(name='title', value=title),
                search.AtomField(name='idpage',value=idpage),
                search.TextField(name='summary', value=summary),
                search.HtmlField(name='content', value=content)
            ]
    )
