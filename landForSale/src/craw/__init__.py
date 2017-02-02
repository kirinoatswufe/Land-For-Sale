#-*- coding:utf-8 -*-

import urllib2
import urllib
import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import urlparse
import os

class LAND:
 
    def __init__(self):
        self.page = 1
        self.title = []
        self.address = []
        self.content = []
        self.statue = []
        self.price = []
        self.size = []
        self.link = []
        self.type = []
        self.subType = []
        self.img = []
        
        
        
    def getPage(self, page):
        try:
            url = 'http://www.loopnet.com/New-York/New-York_Land-For-Sale/' + str(page) + '/'
            html_data = urllib2.urlopen(url).read()
            return html_data
 
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"failed: ",e.reason
                return None


    def getInfo(self, page):
       
        soup = BeautifulSoup(self.getPage(page), 'html.parser', from_encoding='utf-8')
        lands = soup.find_all('span', class_="listingTitle")
        for land in lands:
            self.title.append(land.get_text())
        
        addresses = soup.find_all('div', class_="listingDescription")
        for addr in addresses:
            temp = str(addr.find_all("b"))
            temp = temp.replace("]", '')
            temp = temp.replace("</b>", '')
            temp = temp.split("<b>")
            self.address.append(temp[1])
        
        contents = soup.find_all('span', class_="propertyDescription")
        for content in contents:
            self.content.append(content.get_text())
            
        statues = soup.find_all('div', class_="listingStats")
        for statue in statues:
            self.statue.append(str(statue.contents[0]))
            rest = (statue.find_all("br"))
            a = str(rest[0])
            a = a.replace("</br>", '')
            a = a.split("<br>")
            self.price.append(a[1])
            self.size.append(a[2])
            self.type.append(a[3])
            self.subType.append(a[4])

            
        links = soup.find_all('div', class_="listingDescription")
        for link in links:
            new_url = link.contents[0]['href']
            full_link = urlparse.urljoin("http://www.loopnet.com", new_url)
            self.link.append(full_link)
            
        path = os.getcwd()
        pics = soup.find_all('div', class_="listingPhoto")
        for pic in pics:
            img_src = pic.find('img')['src']
            self.img.append(img_src)
            
            
            
craw = LAND()
craw.getInfo(1)
craw.getInfo(2)

#download pictures
count = 1
for imgsrc in craw.img:
    picName = str(count) + '.jpg' 
    try:
        urllib.urlretrieve(imgsrc, picName)
        print 'Successed' + str(count)
    except Exception, e:
        print 'No photoes'
    count+=1
    
#show info
print craw.title
print craw.content
print craw.statue
print craw.price
print craw.size
print craw.type
print craw.subType
print craw.link
print craw.img

data = {'title': craw.title, 'address': craw.address, 'picture address': craw.img, 'statue': craw.statue, 'content': craw.content, 'price': craw.price, 'size': craw.size, 'type': craw.type, 'subtype': craw.subType, 'link': craw.link}
frame = pd.DataFrame(data)
frame.index.name = 'No'
print frame

frame.to_csv('land_for_sale.csv')
