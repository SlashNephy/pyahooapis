#! python3
# -*- coding: utf-8 -*-

import os
import re
import urllib.request, urllib.parse
from xml.dom import minidom
import json

newline_sub = re.compile('\n').sub
property_match = re.compile('[a-zA-Z].*').match

class Service(object):
	url = 'http://yahoo.co.jp'
	
	def __init__(self, appid, encoding=None):
		self.appid = appid
		if 'PYAHOOAPIS_ENCODING' in os.environ:
			if encoding is not None:
				os.environ['PYAHOOAPIS_ENCODING'] = encoding
		else:
			os.environ['PYAHOOAPIS_ENCODING'] = encoding or 'utf8'

	def _encode_to_utf8(self, text):
		return text
		return str(text, os.environ['PYAHOOAPIS_ENCODING']).encode('utf8')
		
	def _get_text(self, node, tagName):
		try:
			return node.getElementsByTagName(tagName)[0].firstChild.nodeValue
		except:
			return None
	
	def _response(self, params):
		return urllib.request.urlopen(self.url+'?appid=%s&%s' % (self.appid, urllib.parse.urlencode(params))).read()
		
	def _setParam(self, params, param, name, split):
		if param is not None:
			params[name] = split.join(map(str, param))
	
	def _get_dom(self, params):
		params['sentence'] = self._encode_to_utf8(params['sentence'])
		return minidom.parseString(self._remove_newline(self._response(params)))
		
	def _remove_newline(self, xml):
		return newline_sub('', xml.decode())
	
	def _binary2list(self, binary, dct):
		return [dct[key] for key in iter(dct) if binary & key]
	
	def _binary2param(self, split, binary, dct):
		return split.join(map(str, self._binary2list(binary, dct)))
		
	def py2json(self, obj):
		def _py2json(_obj):
			if isinstance(_obj, list):
				return [_py2json(_o) for _o in _obj]
			elif isinstance(_obj, BaseObject):
				properties = (p for p in dir(_obj) if property_match(p))
				return dict((p, _py2json(getattr(_obj, p))) for p in properties)
			else:
				return _obj
		return json.dumps(_py2json(obj), indent=False)
				
class BaseObject(object):
	def encode(self, text):
		return text.encode(os.environ['PYAHOOAPIS_ENCODING'])
