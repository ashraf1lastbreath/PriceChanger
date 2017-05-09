# -*- coding: utf-8 -*-

import requests
import sys
from bs4 import BeautifulSoup
import re
import logging
logging.basicConfig( )

#Scrap URL to fetch data
########################
def flipkart_scrapper(url):
    print "" 
    #include http header fields for Requests   
    headers =   {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate, sdch, br', 
    'Accept-Language' : 'en-US,en;q=0.8',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'
    }
    #fetch response from Requests
    response = requests.get(url, headers=headers)    
    html = response.content            #fetch the entire HTML of the URL
    #print html
     #WorkAround : to solve issue  :"bs4.dammit:Some characters could not be decoded, and were replaced with REPLACEMENT CHARACTER."
    html = html.decode('latin-1')
    soup = BeautifulSoup(html,'html.parser')
    found = False

    #retrieve Item
    try :
        item = soup.find('h1', attrs={'class': '_3eAQiD'})   #to find out only the tag we are interested in
        #print item
        item_txt = item.get_text( ).encode(sys.stdout.encoding, errors='replace' )  #to retrieve the item name text
        item_txt = item_txt.strip( )          # to remove trailing and leading whitespaces
        #print "item_txt : ",item_txt
        found = True
    except:
        item_txt = ""
        found = False
        print "Product not found"

    #Retrieve price
    try :
        price = soup.find('div', attrs={'class': '_1vC4OE _37U4_g'}) 
        price_txt = price.get_text( ).encode(sys.stdout.encoding, errors='replace' )   #to retrieve the item name text
        #Removing Non Numeric symbols from Price
        price_txt = re.sub("[^0-9]", "",price_txt )
        price_txt = int(price_txt)
        found = True
        print "Price found"
    except :
        price_txt = 0
        found = False
        pass

    print  "Present price  of  "+item_txt + " on Flipkart  is Rs. " + str(price_txt)
    print ""
    return (price_txt, item_txt, found )



def amazon_scrapper(url):
    print "" 
    #include http header fields for Requests   
    headers =   {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate, sdch, br', 
    'Accept-Language' : 'en-US,en;q=0.8',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'
    }
    #fetch response from Requests
    response = requests.get(url, headers=headers)    
    html = response.content            #fetch the entire HTML of the URL
    #print html
     #WorkAround : to solve issue  :"bs4.dammit:Some characters could not be decoded, and were replaced with REPLACEMENT CHARACTER."
    html = html.decode('latin-1')
    soup = BeautifulSoup(html,'html.parser')
    found = False

    #retrieve Item
    try :
        #retrieve Item 
        item = soup.find('h1', attrs={'class': 'a-size-large a-spacing-none'})    
        item_txt = item.get_text( ).encode(sys.stdout.encoding, errors='replace' )  #to retrieve the item name text
        item_txt = item_txt.strip( )          # to remove trailing and leading whitespaces
        #print item_txt 
        found = True
    except:
        item_txt = ""
        found = False
        print "Product not found"

    #Retrieve price
    try :
        price = soup.find('span', attrs={'class': 'a-size-medium a-color-price'}) 
        price_txt = price.get_text( ).encode(sys.stdout.encoding, errors='replace' )   #to retrieve the item name text
        #Removing Non Numeric symbols from Price
        price_txt = re.sub("[^0-9]", "",price_txt )
        price_txt = int(price_txt ) / 100
        found = True
        print "Price found"
    except :
        price_txt = 0
        found = False
        pass

    print  "Present price  of  "+item_txt + " on  Amazon  is Rs. " + str(price_txt)
    print ""
    return (price_txt, item_txt, found )



def snapdeal_scrapper(url):
    print "" 
    #include http header fields for Requests   
    headers =   {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate, sdch, br', 
    'Accept-Language' : 'en-US,en;q=0.8',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'
    }
    #fetch response from Requests
    response = requests.get(url, headers=headers)    
    html = response.content            #fetch the entire HTML of the URL
    #print html
     #WorkAround : to solve issue  :"bs4.dammit:Some characters could not be decoded, and were replaced with REPLACEMENT CHARACTER."
    html = html.decode('latin-1')
    soup = BeautifulSoup(html,'html.parser')
    found = False

    #retrieve Item
    try :
         #retrieve Item 
         item = soup.find('h1', attrs={'class': 'pdp-e-i-head'})   #to find out only the tag we are interested in
         item_txt = item.get_text( ).encode(sys.stdout.encoding, errors='replace' )  #to retrieve the item name text
         item_txt = item_txt.strip( )          # to remove trailing and leading whitespaces
         #print item_txt 
         found = True
    except:
        item_txt = ""
        found = False
        print "Product not found"

    #Retrieve price
    try :
        price = soup.find('span', attrs={'class': 'payBlkBig'}) 
        price_txt = price.get_text( ).encode(sys.stdout.encoding, errors='replace' )   #to retrieve the item name text
        #Removing Non Numeric symbols from Price
        price_txt = re.sub("[^0-9]", "",price_txt )
        price_txt = int(price_txt ) 
        found = True
        print "Price found"
    except :
        price_txt = 0
        found = False
        pass

    print  "Present price  of  "+item_txt + " on  Snapdeal  is Rs. " + str(price_txt)
    print ""
    return (price_txt, item_txt, found )
