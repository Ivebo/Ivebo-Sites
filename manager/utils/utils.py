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

import re
import os
import base64
import random

from google.appengine.api import memcache
from google.appengine.api import users

from django.template import defaultfilters

def get_apps():
  apps = os.environ['apps']
  apps1 = []
  if apps:
     apps = apps.split(',')
  for a in apps:
     apps1.append(a.strip())
  return apps1


XSRF_VALIDITY_TIME = 60

def validstring(string):
    #tabla = maketrans(u"ÀÁÂÃÄÅàáâãäåÇçÌÍÎÏìíîïÙÚÛÜùúûüÿÑñ",u"aaaaaaaaaaaaooooooooooooeeeeeeeecciiiiiiiiuuuuuuuuynn")
    string = string.rstrip()
    string = string.lstrip()
    string = string.encode('utf-8').lower();
    string = re.sub(r'(À|Á|Â|Ã|Ä|Å|à|á|â|ã|ä|å)', 'a', string)
    string = re.sub(r'(È|É|Ê|Ë|è|é|ê|ë)', 'e', string)
    string = re.sub(r'(Ì|Í|Î|Ï|ì|í|î|ï)', 'i', string)
    string = re.sub(r'(Ò|Ó|Ô|Õ|Ö|Ø|ò|ó|ô|õ|ö|ø)', 'o', string)
    string = re.sub(r'(Ù|Ú|Û|Ü|ù|ú|û|ü)', 'u', string)
    string = re.sub(r'(Ù|Ú|Û|Ü|ù|ú|û|ü)', 'u', string)
    string = re.sub(r'(Ç|ç)', 'c', string)
    string = re.sub(r'(ÿ)', 'y', string)
    string = re.sub(r'(Ñ|ñ)', 'n', string)
    string = re.sub(r'(´|`|ª|!|\?|\¿)', '', string)
    string = re.sub(r"[^a-z|0-9]", " ", string)
    string = re.sub(r'(-)+', '', string)
    string = re.sub(r'\s+', '-', string)
    return string

def validstringName(string):
    #tabla = maketrans(u"ÀÁÂÃÄÅàáâãäåÇçÌÍÎÏìíîïÙÚÛÜùúûüÿÑñ",u"aaaaaaaaaaaaooooooooooooeeeeeeeecciiiiiiiiuuuuuuuuynn")
    string = re.sub(r"(/|\\|\,|\.)", "", string)
    return string


def _MakeUserStr():
  """Make a user string to use to represent the user.  'noauth' by default."""
  user = users.get_current_user()
  if not user:
    user_str = 'noauth'
  else:
    user_str = user.nickname()

  return user_str

def CreateXsrfToken(action):
  """Generate a token to be passed with a form for XSRF protection.

  Args:
    action: action to restrict token to

  Returns:
    suitably random token which is only valid for ten minutes and, if the user
    is authenticated, is only valid for the user that generated it.
  """
  user_str = _MakeUserStr()
  token = base64.b64encode(''.join([chr(int(random.random()*255)) for _ in range(0, 64)]))
  memcache.add(token,
               (user_str, action),
               time=XSRF_VALIDITY_TIME)

  return token

def ValidateXsrfToken(token, action):
  """Validate a given XSRF token by retrieving it from memcache.

  If the token has not been evicted from memcache (past ten minutes) and the
  user strings are equal, then this is a valid token.

  Args:
    token: token to validate from memcache.
    action: action that token should correspond to

  Returns:
    True if the token exists in memcache and the user strings are equal,
    False otherwise.
  """
  user_str = _MakeUserStr()
  token_obj = memcache.get(token)

  if not token_obj:
    return False

  token_str = token_obj[0]
  token_action = token_obj[1]

  if user_str != token_str or action != token_action:
    return False

  return True

def stringstrip(string):
    stringresult = string.rstrip()
    stringresult = stringresult.lstrip()
    return stringresult

def short_text(text):
    return str(defaultfilters.slugify(text))