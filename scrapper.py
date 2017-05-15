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
    print "scrapping Flipkart URL" 
    #include http header fields for Requests   
    headers =   {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate, sdch, br', 
    'Accept-Language' : 'en-US,en;q=0.8',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'
    }
    #fetch response from Requests
    response = requests.get(url, headers=headers)    
    response.encoding = 'utf-8'      # define encoding at response level itself
    html = response.content            #fetch the entire HTML of the URL
    
    soup = BeautifulSoup(html,'html.parser')
    found = False

    #Scrap from metadata tag for Description or description
    desc= soup.find(attrs={'name':'Description'})
    if desc == None:
        desc= soup.find(attrs={'name':'description'})
    try:
        #print desc['content']
        desc =  desc['content']
    except :
        print "Meta tag Description 'Content' not found"

    #retrieve Item 
    item = str(soup.find('h1', attrs={'class': '_3eAQiD'}))  #to find out only the tag we are interested in
    if item== None :
        try :
            item_txt = str(desc.split("Buy ")[1].split("Rs. " )[0] )  #if not found, try scrapping using Title metadata name : description  
            print "Debug 1 : Item found:", str(item_txt)
            found = True
        except:
            item_txt = " "
            found = False
            print "Error 1 : Product not found"
    else :
        try :
            item_txt = item.get_text( )         #to retrieve the item name text
            item_txt = str(item_txt.strip( ))          # to remove trailing and leading whitespaces
            print "Debug 2 : item_txt  found : ", str(item_txt)
            found = True
        except :
            #extract only text from HTML tag
            item_soup = BeautifulSoup(item,'html.parser')
            item = item_soup.findAll(text=True)
            try :
                item_txt = item[1]
                print "Error 2 : forcibly extracting product from Html tag  : " + str(item_txt)
            except :
                item_txt = item
                print "Error 3 : extracted product from Html tag" + str(item_txt)
            found = True

    #retrieve price
    price = soup.find('div', attrs={'class': '_1vC4OE _37U4_g'}) 
    if price== None :            
        try :
            price_txt = int(desc.split("Rs. ")[1].split(" ")[0] )                #if not found, try scrapping using Title metadata name : description 
            print "Debug 1 : Price found :",str(price_txt)
            found = True
        except :
            price_txt = 0
            found = False
            print "Error 1 : Price not found"
            pass
    else :
        try :
            price_txt = price.get_text( )          #to retrieve the item name text
            #Removing Non Numeric symbols from Price
            price_txt = re.sub("[^0-9]", "",price_txt )
            price_txt = int(price_txt)
            print "Debug 2 : Price found :",str(price_txt)
            found = True
        except :
            price_txt = 0
            found = False
            print "Error 2 : Price not found"
            pass

    print  "Present price  of  " + str(item_txt ) + " on Flipkart is Rs. " + str(price_txt)
    #print  "Present price  on Flipkart is Rs. ", price_txt
    print ""
    return (price_txt, item_txt, found )



def amazon_scrapper(url):
    print ""
    print "scrapping Amazon URL"
    #include http header fields for Requests   
    headers =   {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate, sdch, br', 
    'Accept-Language' : 'en-US,en;q=0.8',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'
    }
    #fetch response from Requests
    response = requests.get(url, headers=headers)    
    response.encoding = 'utf-8'      # define encoding at response level itself
    html = response.content             #fetch the entire HTML of the URL

    soup = BeautifulSoup(html,'html.parser')
    found = False

    #retrieve Item
    item = soup.find('h1', attrs={'class': 'a-size-large a-spacing-none'})
    if item == None:
        try :
            item = soup.find('h1', attrs={'class': 'a-size-large a-spacing-none'})
            item_txt = item.get_text( ).encode(sys.stdout.encoding, errors='replace' )
            item_txt = item_txt.strip( )          # to remove trailing and leading whitespaces
            print "Debug 1 : item_txt found :", item_txt 
            found = True
        except :
            item_txt = ""
            found = False
            print "Error 1 : Product not found"
    else :
        item_txt = item.get_text( )  #to retrieve the item name text
        item_txt = str(item_txt.strip( ) )         # to remove trailing and leading whitespaces
        print "Debug 2 : item_txt found :" + str(item_txt )
        found = True

    #retrieve price
    price = soup.find('span', attrs={'class': 'a-size-medium a-color-price'}) 
    if price ==None:
        try :
            price = soup.find('span', attrs={'class': 'a-size-medium a-color-price'}) 
            price_txt = price.get_text( ).encode(sys.stdout.encoding, errors='replace' )  #to retrieve the item name text
            #Removing Non Numeric symbols from Price
            price_txt = re.sub("[^0-9]", "",price_txt )
            price_txt = int(price_txt ) / 100
            found = True
            print "Debug 1 : Price found :" + str(price_txt)
        except :
            price_txt = 0
        found = False
        print "Error 1 : Price not found"
        pass
    else :
        try :
            price = soup.find('span', attrs={'class': 'a-size-medium a-color-price'}) 
            price_txt = price.get_text( ) #to retrieve the item name text
            #Removing Non Numeric symbols from Price
            price_txt = re.sub("[^0-9]", "",price_txt )
            price_txt = int(price_txt ) / 100
            found = True
            print "Debug 2 : Price found :" + str(price_txt)
        except :
            price_txt = 0
            found = False
            print "Error 2 : Price not found"
            pass

    print  "Present price  of  "+item_txt + " on  Amazon  is Rs. " + str(price_txt)
    print ""
    return (price_txt, item_txt, found )



def snapdeal_scrapper(url):
    print ""
    print "scrapping Snapdeal URL" 
    #include http header fields for Requests   
    headers =   {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate, sdch, br', 
    'Accept-Language' : 'en-US,en;q=0.8',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'
    }
    #fetch response from Requests
    response = requests.get(url, headers=headers)    
    response.encoding = 'utf-8'
    html = response.content            #fetch the entire HTML of the URL
    #print html
     #WorkAround : to solve issue  :"bs4.dammit:Some characters could not be decoded, and were replaced with REPLACEMENT CHARACTER."
    #html = html.decode('latin-1')
    #html = html.decode('utf-8', 'ignore')
    soup = BeautifulSoup(html,'html.parser')
    #print html
    found = False

    #retrieve Item
    try :
         #retrieve Item 
         item = soup.find('h1', attrs={'class': 'pdp-e-i-head'})   #to find out only the tag we are interested in
         #print item
         #item_txt = item.get_text( ).encode(sys.stdout.encoding, errors='replace' )  #to retrieve the item name text
         item_txt = item.get_text( )
         item_txt = str(item_txt.strip( ) )         # to remove trailing and leading whitespaces
         #print item_txt 
         found = True
    except:
        item_txt = ""
        found = False
        print "Product not found"

    #Retrieve price
    try :
        print "getting price"
        price = soup.find('span', attrs={'class': 'payBlkBig'}) 
        price_txt = price.get_text( )  #to retrieve the item name text
        #Removing Non Numeric symbols from Price
        price_txt = re.sub("[^0-9]", "",price_txt )
        print price_txt
        price_txt = int(price_txt ) 
        found = True
        print "Price found" + str(price_txt)
    except :
        price_txt = 0
        found = False
        pass

    print  "Present price  of  "+item_txt + " on  Snapdeal  is Rs. " + str(price_txt)
    print ""
    return (price_txt, item_txt, found )
