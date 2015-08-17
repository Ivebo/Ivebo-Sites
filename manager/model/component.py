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

#Library
from manager.utils.utils import *
from manager.utils.genID import PushID

import os
    
class Component(ndb.Model):
    title = ndb.StringProperty(required=True)
    title_short = ndb.StringProperty(required=True)
    idcomponent = ndb.StringProperty(required=True)
    gs_filename = ndb.StringProperty()
    summary = ndb.StringProperty()
    date_publication = ndb.DateTimeProperty(auto_now_add=True)
    date_updated = ndb.DateTimeProperty(auto_now=True)
    userID = ndb.StringProperty(required=True)
    visibility = ndb.StringProperty(choices=set(['public','private']),required=True,default='public')


def title_short(string):
    string = short_text(string)
    return string

def GenId():
    p = PushID()
    p = p.next_id()
    return p

def site_key():
  return ndb.Key('Site', os.environ['site'])
