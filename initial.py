# -*- coding: utf-8 -*-

import sys
import re
import twitter
import requests
import pymongo
from pymongo import MongoClient
from ConfigParser import SafeConfigParser
import httplib
import urlparse

from scrapper import flipkart_scrapper

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


            price = flipkart_scrapper(url)
            #print mention
            isnew = mongo_post(status_id, screen_name, url, price)
            #post tweet only if it is new
            if isnew:
                Tw_post(screen_name, price,  status_id)

        except requests.exceptions.MissingSchema:
            print "Tweet status doesnt have any url"    



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