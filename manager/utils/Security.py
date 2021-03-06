﻿# -*- coding: utf-8 -*-
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
#along with this program.  If not, see <http://www.gnu.org/licenses/>
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from BeautifulSoup import BeautifulSoup

class FilterXSS:
    def __init__(self,entrada):
        self.htmlentrada = entrada
        
    def clean(self):
        self.htmlentrada = self.htmlentrada.replace("&lt;", "<")
        self.htmlentrada = self.htmlentrada.replace("&gt;", ">")
        soup = BeautifulSoup(self.htmlentrada) 
        allscript = soup.findAll(lambda tag: len(tag.attrs) > 1)
        for tag in allscript:
            del tag['style']
        allscript = soup.findAll(['script','iframe','object','embed','head','body','a','frame','img'])
        for tag in allscript:
            tag.extract()
        #Optimizado 
        #[tag.extract() for tag in allscript]
        return soup
        