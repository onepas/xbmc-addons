# -*- coding: utf-8 -*-
import urllib
import urllib2
import os
import urlfetch
import re
import random

from BeautifulSoup import BeautifulSoup

def make_request(url, headers=None):
    if headers is None:
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
                   'Referer' : 'http://www.google.com'}
    try:
        req = urllib2.Request(url,headers=headers)
        f = urllib2.urlopen(req)
        body=f.read()
        return body
    except urllib2.URLError, e:
        print 'We failed to open "%s".' % url
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        if hasattr(e, 'code'):
            print 'We failed with error code - %s.' % e.code

def build_menu():
	content = make_request('http://megabox.vn/')
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.find('div',{'class' : 'navTop'}).findAll('div')

	for item in items:
		if item.parent.a.text != u'Thiết Bị':
			print item.parent.a.text + ' ' + item.parent.a.get('href')
			subItems = item.findAll('li')
			for subItem in subItems:
				if subItem.get('style') is None and subItem.a.get('style') is None:
					print subItem.a.text + ' ' + subItem.a.get('href')


build_menu()