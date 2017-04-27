# -*- coding: utf-8 -*-

import sys
import re
import requests
from bs4 import BeautifulSoup
import twitter
import pymongo
from pymongo import MongoClient
from ConfigParser import SafeConfigParser
import httplib
import urlparse

#remove encoding etc appearing in url after '?' character 
def removeURLencoding(url):
   head, sep, tail = url.partition('?')
   return head

#Function to prevent twitter from shortening the URL
def unshorten_url(url):
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc)
    h.request('HEAD', parsed.path)
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    else:
        return url


 #1. Fetch Twitter Data
####################Fetch Data for Mentions on TwitterHandle
def get_Twdata(  api):
    mentions=api.GetMentions( )   
    print ""

    for mention in mentions:
        msg =  mention.text
        status_id =  mention.id
        url = msg[15:]

        screen_name = mention.user.screen_name

        try:
            url = unshorten_url(url)
            url = removeURLencoding(url)

            #logic to compare Amazon, flipkart, snapdeal goes here


            price = scrapper(url)
            #print mention
            isnew = mongo_post(status_id, screen_name, url, price)
            #post tweet only if it is new
            if isnew:
                Tw_post(screen_name, price,  status_id)

        except requests.exceptions.MissingSchema:
            print "Tweet status doesnt have any url"    


#2. Scrap URL to fetch data
########################
def scrapper(url):
    print "" 
    #include http header fields for Requests   
    headers =   {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate, sdch, br', 
    'Accept-Language' : 'en-US,en;q=0.8',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }
    #fetch response from Requests
    response = requests.get(url, headers=headers)    
    html = response.content            #fetch the entire HTML of the URL
    soup = BeautifulSoup(html,'html.parser')

    #retrieve Item
    item = soup.find('h1', attrs={'class': '_3eAQiD'})   #to find out only the tag we are interested in
    item_txt = item.get_text( ).encode(sys.stdout.encoding, errors='replace' )  #to retrieve the item name text
    item_txt = item_txt.strip( )          # to remove trailing and leading whitespaces
    #print "item_txt : ",item_txt

    #Retrieve price
    price = soup.find('div', attrs={'class': '_1vC4OE _37U4_g'}) 
    price_txt = price.get_text( ).encode(sys.stdout.encoding, errors='replace' )   #to retrieve the item name text
    #Removing Non Numeric symbols from Price
    price_txt = re.sub("[^0-9]", "",price_txt )
    price_txt = int(price_txt)

    print  "Present price  of  "+item_txt  + " on Flipkart  is :" + str(price_txt)
    print ""
    return (price_txt )


#3.Post to MongoDb
####################
def mongo_post(status_id, screen_name, url, price):   
    parser = SafeConfigParser( )
    parser.read('config.ini')

    is_replied = False
    connection = MongoClient(parser.get('mongo_server', 'mongo_url'))
    db = connection.pricechanger.Message
    pricechanger ={ }    
    pricechanger = {'status_id':status_id, 'url':url, 'screen_name':screen_name, 'price':int(price), 'is_replied':is_replied}

    try:
        db.insert_one(pricechanger)
    except pymongo.errors.DuplicateKeyError:
        print "Duplicate Entry  for same Status Id"
        return False

    print " Data Posted to Database ..."
    return True
    #connection.close()


#4. Post Reply to Twitter Mentions
################################
def Tw_post( screen_name, price,  status_id):
    try:
        status = api.PostUpdate( str("@"+screen_name) + "   Initial  Price  of your item is Rs. " +str(price),in_reply_to_status_id=str(status_id))
        print status.text
        print "Posted on Twitter"
    except twitter.error.TwitterError:
        print "Duplicate Tweet !!"



#Set up twitter API data
#############################################################
parser = SafeConfigParser()
parser.read('config.ini')

#read API data from 'config.ini'  file
api = twitter.Api(consumer_key = parser.get('twitter_API', 'consumer_key'),
                      consumer_secret = parser.get('twitter_API', 'consumer_secret'),
                      access_token_key = parser.get('twitter_API', 'access_token_key'),
                      access_token_secret = parser.get('twitter_API', 'access_token_secret'))

get_Twdata( api )      