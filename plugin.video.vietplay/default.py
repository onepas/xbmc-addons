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
import json
import time
import xbmc,xbmcplugin,xbmcgui,xbmcaddon
import pyfscache

from BeautifulSoup import BeautifulSoup

addon      = xbmcaddon.Addon('plugin.video.vietplay')
profile    = xbmc.translatePath(addon.getAddonInfo('profile'))
mysettings = xbmcaddon.Addon(id='plugin.video.vietplay')
home       = mysettings.getAddonInfo('path')
fanart     = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon       = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos      = xbmc.translatePath(os.path.join(home, 'logos\\'))
fptplay    = 'http://fptplay.net/'

cachePath = xbmc.translatePath( os.path.join( home, 'cache' ) )
cache = pyfscache.FSCache(cachePath, days=7)

__thumbnails = []

def messageBox(title='VietMovie', message = 'message'):
    dialog = xbmcgui.Dialog()
    dialog.ok(str(title), str(message))

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

def setCache(key,value):
    try:
        cache.expire(key)
    except:
        pass
    try:
        cache[key] = value
    except:
        pass

def getCache(key):
    try:
        value = cache[key]
        return value
    except:
        return None

def clearCache():
    try:
        cache.purge()
    except:
        pass

def get_thumbnail_url():
    global __thumbnails
    url = ''
    try:
        if len(__thumbnails) == 0:
            content = getCache('thumbnails')
            if content == None:
                content = make_request('https://raw.github.com/onepas/xbmc-addons/master/thumbnails/thumbnails.xml')
                setCache('thumbnails',content)

            soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
            __thumbnails = soup.findAll('thumbnail')

        url = random.choice(__thumbnails).text 
    except:
        pass
      
    return url

def _makeCookieHeader(cookie):
	cookieHeader = ""
	for value in cookie.values():
		cookieHeader += "%s=%s; " % (value.key, value.value)
	return cookieHeader


def home():
	link = getCache('home')
	if link == None:
		link=make_request(fptplay)
		setCache('home', link)
	
	match=re.compile('<ul class="top_menu reponsive">(.+?)</ul>',re.DOTALL).findall(link)
	if len(match) > 0:
		link = match[0]
		match=re.compile("<a href=\"(.+?)\"\s*class=\".+?\">(.+?)<\/a>").findall(link)
		for url,name in match:
			addDir( name , fptplay + url ,1, get_thumbnail_url())	

	
	addDir('Thuý Nga - Tổng hợp','http://ott.thuynga.com/vi/genre/index/22/3', 200, get_thumbnail_url())
	addDir('Thuý Nga - Hài kịch','http://ott.thuynga.com/vi/genre/index/26/3', 200, get_thumbnail_url())
	addDir('Thuý Nga - Hậu trường','http://ott.thuynga.com/vi/genre/index/64/3', 200, get_thumbnail_url())

	addDir('Tìm kiếm',fptplay, 100, get_thumbnail_url())	
	addDir('Xóa cache',fptplay, 1000, get_thumbnail_url())		
								
								
def show_thuy_nga_list(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.4) Gecko/2008092417 Firefox/4.0.4')
	response = urllib2.urlopen(req, timeout=90)
	content=response.read()
	response.close()

	thuyngaUrl = 'http://ott.thuynga.com/'

	match=re.compile('<div class="image-wrapper">.*?<a href="(.*?)" style="background-image: url\(\'(.*?)\'\)".*?<h3>.*?<a href=".*?">(.*?)</a>.*?</h3>.*?<div class="content">.*?<p>(.*?)</p>.*?</div>.*?<div style="clear:both;"></div>',re.DOTALL).findall(content)
	for url,thumbnail,title,summary in match:	
		addDir(title,thuyngaUrl + url,299,thumbnail + '?f.png',plot=summary,playable=True)

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

def plist(url,page = 0):	
	for page in range(1,20):
		url_with_page = url + '/' + str(page)
		json_data=make_request(url_with_page)
		match=json.loads(json_data)
		if len(match['videos_list']) == 0:
			break
		for video in match['videos_list']:
			title = video['title']
			thumbnail = video['thumb']
			description = video['description']
			link_video = video['link_video']
			episode_type = video['episode_type']
			if 'Single' in episode_type:
				addDir( title.encode('utf8'),fptplay + link_video,4,thumbnail,plot=description,playable=True)
			else:
				addDir( title.encode('utf8'),fptplay + link_video,4,thumbnail,plot=description)


def dirs(url):
	link=make_request(url)
	
	match=re.compile('<a class="col-xs-12 link_title_header" href="/the-loai-more/(.+?)/1">\s*<span class="pull-left" >(.+?)</span >').findall(link)
	
	for url,name in match:	
		addDir(name,fptplay + 'get_all_vod_structure/news/' + url,2, get_thumbnail_url(), page=1)

def episodes(url):

	link=make_request(url)
	title=re.compile('<title >([^\']+)</title >').findall(link)	
	title = title[-1].replace('&#39;',"'")
	match=re.compile('<div class="eps_vod caption">\s*<a data="(.+?)".+?>(.+?)</a>',re.DOTALL).findall(link)
	if len(match) > 0:
		for url,name in match:
			addDir(('%s   -   %s' % (name,title)),('%s%s' % (fptplay, url)),5, get_thumbnail_url(),playable=True)
	else:
		match=re.compile("CallGetVOD\('(.+?)', '(.+?)', currentChapter\);").findall(link)
		if len(match) > 0:
			url = fptplay + 'getvod/' + match[0][0] + '/' + match[0][1] + '/1'
			vlinks(url,'')
											

def vlinks(url,name):
	link=make_request(url)
	listitem = xbmcgui.ListItem(path=link)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def search():
	query = common.getUserInput('Tìm kiếm Phim', '')
  	if query is None:
		return
	url = fptplay + '/search/' + urllib.quote_plus(query)

	link=make_request(url)
	match=re.compile('<a href="(.+?)" title="(.+?)" class="item_image">\s*<img src="(.+?)".+?').findall(link)

	for url,name, thumbnail in match:
		title = name.replace('&#39;',"'")
		addDir( title,fptplay + url,4,thumbnail,playable=True)

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

def addDir(name,url,mode,iconimage,page=0,plot='',playable=False):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&page="+str(page)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    isFolder = True
    liz.setInfo( type="Video", infoLabels={ "Title": name, "plot":plot } )
    if playable:
    	liz.setProperty('IsPlayable', 'true')
    	isFolder = False
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
    return ok
                      

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

params=get_params()

url=None
name=None
mode=None
page=0

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

try:
    page=int(params["page"])
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
    plist(url,page)
			
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
			
elif mode==1000:
   	clearCache()
xbmcplugin.endOfDirectory(int(sys.argv[1]))