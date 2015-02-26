# -*- coding: utf-8 -*-

'''
Copyright (C) 2014                                                     

This program is free software: you can redistribute it and/or modify   
it under the terms of the GNU General Public License as published by   
the Free Software Foundation, either version 3 of the License, or      
(at your option) any later version.                                    

This program is distributed in the hope that it will be useful,        
but WITHOUT ANY WARRANTY; without even the implied warranty of         
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          
GNU General Public License for more details.                           

You should have received a copy of the GNU General Public License      
along with this program. If not, see <http://www.gnu.org/licenses/  
'''                                                                           
import CommonFunctions as common
import urllib,urllib2,re,os
import random
import time
import xbmc,xbmcplugin,xbmcgui,xbmcaddon
from BeautifulSoup import BeautifulSoup

addon      = xbmcaddon.Addon('plugin.video.vietplay')
profile    = xbmc.translatePath(addon.getAddonInfo('profile'))
mysettings = xbmcaddon.Addon(id='plugin.video.vietplay')
home       = mysettings.getAddonInfo('path')
fanart     = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon       = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos      = xbmc.translatePath(os.path.join(home, 'logos\\'))
fptplay    = 'http://fptplay.net/'

__thumbnails = []

def _makeCookieHeader(cookie):
	cookieHeader = ""
	for value in cookie.values():
		cookieHeader += "%s=%s; " % (value.key, value.value)
	return cookieHeader

def make_request(url, params = None,  headers=None):
	if headers is None:
		headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
	           'Referer' : 'http://www.google.com'}
	try:
		data = None
		if params is not None:
		  	data = urllib.urlencode(params)
		req = urllib2.Request(url,data,headers)
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

def get_thumbnail_url():
	global __thumbnails
	url = ''
	try:
		if len(__thumbnails) == 0:
			content = make_request('https://raw.github.com/onepas/xbmc-addons/master/thumbnails/thumbnails.xml')
			soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
			__thumbnails = soup.findAll('thumbnail')

		url = random.choice(__thumbnails).text 
	except:
		pass

	return url

def home():
	req = urllib2.Request(fptplay)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.4) Gecko/2008092417 Firefox/4.0.4')
	response = urllib2.urlopen(req, timeout=90)
	link=response.read()
	response.close()
	match=re.compile("<li ><a href=\"(.+?)\" class=\".+?\">(.+?)<\/a><\/li>").findall(link)
	for url,name in match:
		if 'livetv' in url:
			print url
			#addDir('[COLOR yellow]' + name + '[/COLOR]',fptplay + url,3,logos + 'fptplay.png')
		else:
			addDir( name , fptplay + url ,1, get_thumbnail_url())	

	addDir('Thuý Nga - Tổng hợp','http://ott.thuynga.com/vi/genre/index/22/3', 200, get_thumbnail_url())
	addDir('Thuý Nga - Hài kịch','http://ott.thuynga.com/vi/genre/index/26/3', 200, get_thumbnail_url())
	addDir('Thuý Nga - Hậu trường','http://ott.thuynga.com/vi/genre/index/64/3', 200, get_thumbnail_url())

	addDir('Tìm kiếm',fptplay, 100, get_thumbnail_url())		
								
								
def show_thuy_nga_list(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.4) Gecko/2008092417 Firefox/4.0.4')
	response = urllib2.urlopen(req, timeout=90)
	content=response.read()
	response.close()

	thuyngaUrl = 'http://ott.thuynga.com/'

	match=re.compile('<div class="image-wrapper">.*?<a href="(.*?)" style="background-image: url\(\'(.*?)\'\)".*?<h3>.*?<a href=".*?">(.*?)</a>.*?</h3>.*?<div class="content">.*?<p>(.*?)</p>.*?</div>.*?<div style="clear:both;"></div>',re.DOTALL).findall(content)
	for url,thumbnail,title,summary in match:	
		addDir(title,thuyngaUrl + url,299,thumbnail + '?f.png',summary)

	match=re.compile('<ul>(.*?)<div class="next button">.*?</ul>').findall(content)
	if len(match) > 0:
		content = match[0]
		match=re.compile('<li><a href="(.*?)">(.*?)</a></li>').findall(content)
		for url,name in match:	
			addDir('[COLOR lime]Trang ' + name + '[/COLOR]', url, 200, get_thumbnail_url())

def show_thuy_nga_play(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.4) Gecko/2008092417 Firefox/4.0.4')
	response = urllib2.urlopen(req, timeout=90)
	content=response.read()
	response.close()

	match=re.compile('var iosUrl = \'(.*?)\';').findall(content)
	if len(match) > 0:
		link = match[0]
		listitem = xbmcgui.ListItem(path=link)
      	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
def plist(url):	
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.4) Gecko/2008092417 Firefox/4.0.4')
	response = urllib2.urlopen(req, timeout=90)
	link=response.read()
	response.close()
	match=re.compile("<div class=\"col\">\s*<a href=\"([^\"]+)\">\s*<img src=\"([^\"]*)\" alt=\"(.+?)\"").findall(link)
	for url,thumbnail,name in match:	
		addDir(name.replace('&#39;',"'"),fptplay + url,4,thumbnail)
	match=re.compile("<li><a href=\"(.+?)\">(\d+)<\/a><\/li>").findall(link)
	for url,name in match:	
		addDir('[COLOR lime]Trang ' + name + '[/COLOR]',fptplay + url,2,logos + 'fptplay.png')

def dirs(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.4) Gecko/2008092417 Firefox/4.0.4')
	response = urllib2.urlopen(req, timeout=90)
	link=response.read()
	response.close()
	match=re.compile("<h3><a href=\"(.+?)\">(.+?)<\/a><\/h3>").findall(link)
	for url,name in match:	
		addDir(name.replace('&#39;',"'"),fptplay + url,2,  get_thumbnail_url())

def episodes(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.4) Gecko/2008092417 Firefox/4.0.4')
	response = urllib2.urlopen(req, timeout=90)
	link=response.read()
	response.close()
	title=re.compile('<title>([^\']+)</title>').findall(link)		
	match=re.compile("<li class=\"(.*?)\" data=\"(.*?)\" href=\"\/Video([^\"]*)\" onclick=\".*?\"><a>(.*?)<\/a><\/li>", re.MULTILINE).findall(link)
	for cls,data,url,name in match:
		addDir(('%s   -   %s' % ('Tập ' + name,title[-1].replace('&#39;',"'"))),('%s%s' % (fptplay, data)),5, get_thumbnail_url())
						
def index(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.4) Gecko/2008092417 Firefox/4.0.4')
	response = urllib2.urlopen(req, timeout=90)
	link=response.read()
	response.close()
	match=re.compile("channel=\"(.*?)\" href=\"(.+?)\" data=\".+?\">\s+<img src=\"(.*?)\"").findall(link)
	for name,url,thumbnail in match:
		addDir('[COLOR lime]' + name + '[/COLOR]',fptplay + url,5,thumbnail)						

def addLink(name,url,iconimage):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok
			
def vlinks(url,name):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.4) Gecko/2008092417 Firefox/4.0.4')
	req.add_header('Referer', fptplay)
	response = urllib2.urlopen(req, timeout=90)
	link=response.read()
	response.close()

	if 'livetv' in url:
		match=re.compile('var video_str = "<video id=\'main-video\' src=\'" \+ "(.+?)"').findall(link)
		for url in match:
			addLink(name,url.replace('1000.stream','2500.stream'),logos + 'fptplay.png')						
	else:
		listitem = xbmcgui.ListItem(path=link)
      	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def search():
	query = common.getUserInput('Tìm kiếm Phim', '')
  	if query is None:
		return
	url = fptplay + '/Search/' + urllib.quote_plus(query)
	plist(url)

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
                        
    return param

def addDir(name,url,mode,iconimage,plot=''):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    isFolder = True
    liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":plot } )
    if mode == 5 or mode ==299:
    	liz.setProperty('IsPlayable', 'true')
    	isFolder = False
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
    return ok
                      
params=get_params()
url=None
name=None
mode=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
    print ""
    home()
		
elif mode==1:
    print ""+url
    dirs(url)
		
elif mode==2:
    print ""+url
    plist(url)
		
elif mode==3:
    print ""+url
    index(url)
		
elif mode==4:
    print ""+url
    episodes(url)
		
elif mode==5:
   	vlinks(url,name)

elif mode==200:
   	show_thuy_nga_list(url)

elif mode==299:
   	show_thuy_nga_play(url)

elif mode==100:
   	search()
			
xbmcplugin.endOfDirectory(int(sys.argv[1]))