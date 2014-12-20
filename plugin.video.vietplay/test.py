# -*- coding: utf-8 -*-

import urllib,urllib2,re,os

fptplay    = 'http://fptplay.net/'


def episodes(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.4) Gecko/2008092417 Firefox/4.0.4')
	response = urllib2.urlopen(req, timeout=90)
	link=response.read()
	response.close()
	title=re.compile('<title>([^\']+)</title>').findall(link)		
	print title[0]
	match=re.compile("<li class=\"(.*?)\" data=\"(.*?)\" href=\"\/Video([^\"]*)\"><a>(.*?)<\/a><\/li>", re.MULTILINE).findall(link)
	#print match
	for cls,data,url,name in match:
		print data
		#addDir(('%s   -   %s' % ('[COLOR lime]Tập ' + name + '[/COLOR]','[COLOR yellow]' + title[-1] + '[/COLOR]')),('%s/Video%s' % (fptplay, url)),5,logos + 'fptplay.png')
				
episodes('http://fptplay.net/Video/the-x-factor-uk-season-11/1')

req = urllib2.Request('http://fptplay.net/apigetvideo/the-x-factor-uk-season-11/14')
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.4) Gecko/2008092417 Firefox/4.0.4')
req.add_header('Referer', fptplay)
response = urllib2.urlopen(req, timeout=90)
link=response.read()
response.close()

print link