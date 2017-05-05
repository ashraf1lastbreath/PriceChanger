# -*- coding: utf-8 -*-

import twitter
import requests
import pymongo
import os
from pymongo import MongoClient
from ConfigParser import SafeConfigParser

from scrapper import flipkart_scrapper, amazon_scrapper, snapdeal_scrapper
from utils import removeURLencoding , find_domain , unshorten_url


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
            domain = find_domain(url)

            if domain== 'www.flipkart.com':
                scrapped = flipkart_scrapper(url) 
                price = scrapped[0]
                item   = scrapped[1]

            elif domain== 'www.amazon.in':
                scrapped = amazon_scrapper(url)
                price = scrapped[0]
                item   = scrapped[1]

            elif domain== 'www.snapdeal.com':
                scrapped = snapdeal_scrapper(url)
                price = scrapped[0]
                item   = scrapped[1]
            else :
                raise NotImplementedError ("This domain is not supported yet in our system. Be back Later !")

            #post tweet only if it is new    
            isnew = mongo_post(status_id, screen_name, url, price, item)
            if isnew:
                Tw_post(screen_name, price,  status_id, item)

        except requests.exceptions.MissingSchema:
            print "Tweet status doesnt have any url"    


#3.Post to MongoDb
####################
def mongo_post(status_id, screen_name, url, price, item):   
    parser = SafeConfigParser( )
    parser.read('config.ini')

    is_replied = False
    #connection = MongoClient(parser.get('mongo_server', 'mongo_url'))
    connection = os.environ['mongo_url']
    db = connection.pricechanger.Message
    pricechanger ={ }    
    pricechanger = {'status_id':status_id, 'url':url, 'screen_name':screen_name, 'price':int(price), 'item':item, 'is_replied':is_replied}

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
def Tw_post( screen_name, price,  status_id, item):
    try:
        status = api.PostUpdate( str("@"+screen_name) + "  Initial Price of " + item[:85] + " is Rs. " +str(price),in_reply_to_status_id=str(status_id))
        print status.text
        print "Posted on Twitter"
    except twitter.error.TwitterError:
        print "Duplicate Tweet !!"



#Set up twitter API data from config file
#############################################################
#parser = SafeConfigParser()
#parser.read('config.ini')



   

def initial():
    #read API data from 'config.ini'  file
    print "Running parser"
    api = twitter.Api(consumer_key = os.environ['consumer_key'],    
                      consumer_secret = os.environ['consumer_secret'],
                      access_token_key =  os.environ['access_token_key'],
                      access_token_secret =  os.environ['access_token_secret']
    get_Twdata( api ) 
                      
    
