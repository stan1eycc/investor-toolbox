#!/usr/bin/env python
# coding: utf-8

# XXX License
# Copyright (C)

# In[1]:


import requests
import json

from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup as bs


# In[2]:


# Convert ISIN to Bloomberg ticker from Google

def isin2bbg(isin_ticker):
    url = 'https://www.google.com.tw/search'  
    keys = '+fundinfo+bloomberg'
    key_url = 'product'
        
    # Search on Google
    r = requests.get( url, params = {'q': isin_ticker + keys } )
    #print(r.url)
    
    if r.status_code == requests.codes.ok:  
      
        soup = bs(r.text, 'html.parser')
        items = soup.select('div.g')

        if len(items) < 1:
            return -1
        
        for item in items:
            s = item.find('a').get('href')
            link = parse_qs(urlparse(s)[4])['q'][0]            
            parsed_link = urlparse(link)
            
            if key_url in parsed_link[2]:
                s = item.find('span', class_='st').text
                i = s.find("Bloomberg Code,")
                
                return s[i+16:i+23] + ':' + s[i+24:i+26]
            
    return -1


# In[3]:


# Convert Bloomberg to ISIN from Google

def bbg2isin(bbg_ticker):
    url = 'https://www.google.com.tw/search'  
    keys = '"+fundinfo+isin'
    key_url = 'product'
        
    # Search on Google
    r = requests.get( url, params = {'q': '"' + bbg_ticker + keys } )
    #print(r.url)
    
    if r.status_code == requests.codes.ok:
        
        soup = bs(r.text, 'html.parser')
        items = soup.select('div.g')
        
        if len(items) < 1:
            return -1
        
        for item in items:           
            s = item.find('a').get('href')
            link = parse_qs(urlparse(s)[4])['q'][0]
            parsed_link = urlparse(link)
            
            if key_url in parsed_link[2]:
                s = item.find('span', class_='st').text
                i = s.find("ISIN,")                
                
                return s[i+6:i+18]
    return -1


# In[4]:


# Convert ISIN to Morningstar ticker

def isin2morningstar(isin_ticker):
    url = 'https://www.google.com.tw/search'  
    keys = '+morningstar'
        
    # Search on Google
    r = requests.get( url, params = {'q': isin_ticker + keys } )
    #print(r.url)
    
    if r.status_code == requests.codes.ok:  
          
        soup = bs(r.text, 'html.parser')

        items = soup.select('div.g > h3.r > a')
        
        if len(items) > 0:
            #print(items[0])
            s = items[0].get('href')
            ms_link = parse_qs(urlparse(s)[4])['q'][0]
            
            parsed_link = urlparse(ms_link)
            
            if 'morningstar' not in parsed_link[1]:
                return -1
            else:                
                return parse_qs(urlparse(ms_link)[4])['id'][0]
                        
    return -1


# In[5]:


# Convert Bloomberg to morningstar ticker

def bbg2morningstar(bbg_ticker):
    return isin2morningstar(bbg2isin(bbg_ticker))


# In[6]:


# Convert ISIN to Financial Times symbol

def isin2ft(isin_ticker):
    url = 'http://markets.ft.com'
    
    # Search on financial times
    r = requests.get( url + '/data/search', params = {'query':isin_ticker})
    
    if r.status_code == requests.codes.ok:
        soup = bs(r.text, "html.parser")
        tb = soup.find('table', class_='mod-ui-table mod-ui-table--freeze-pane')      
        tr = tb.findAll('tr')
                
        if len(tr)!= 1:
            return
        
        td = tr[0].find('td')
        href = td.find('a').get('href')
        name = td.text
        
        #print(href)
        #print(name)
        
        td = td.find_next_sibling()
        symbol = td.text
        #print(symbol)
    
        r = requests.get(url + href)
        #print(r.url)
        if r.status_code == requests.codes.ok:
            soup = bs(r.text, "html.parser")
            
            k = soup.find('section', class_='mod-tearsheet-add-to-watchlist')
            js = json.loads(str(k.get('data-mod-config')))
            
            xid = js['xid']
            #print(xid)
    
            return xid
    return


# In[7]:


# Testing

if __name__ == "__main__":
    print(isin2bbg('LU0270844359'))
    print(bbg2isin('FAPPAUI:LX'))
    print(bbg2morningstar('FAPPAUI:LX'))
    print(isin2ft('LU0270844359'))

