# -*- coding: utf-8 -*-

import twitter
import requests
from pymongo import MongoClient
from ConfigParser import SafeConfigParser

from scrapper import flipkart_scrapper, amazon_scrapper, snapdeal_scrapper
from utils import  removeURLencoding, find_domain, unshorten_url


#1. Retrieve Data from MongoDb :
################################ 
def mongo_retrieve( ):
    parser = SafeConfigParser( )
    parser.read('config.ini')

    connection = MongoClient(parser.get('mongo_server', 'mongo_url'))
    db = connection.pricechanger.Message

    results = db.find({'is_replied': False})
    print " "
    print " Fetching Data from MongoDb :"
    print "==========================="
    for record in results:
        print record
        newprice = isPriceDecreased(record['url'],record['price'])
        if newprice > 0:
            Tw_reduce_post(record['screen_name'], newprice, record['status_id'])
            db.find_one_and_update(
                {'_id': record['_id']},
                {'$set': {'is_replied': True}}
            )
            

#3. Post  Price Reduction Notification on Twitter :
########################################## 
def Tw_reduce_post(screen_name, price,  status_id ):
    status = api.PostUpdate( str("@"+screen_name) + "  Price of your item has reduced to  Rs. " +str(price),in_reply_to_status_id=str(status_id))
    print(status.text)
    print "Posted on Twitter"


#4. Compare price from Database and price from scrapper again:
####################################################### 
def isPriceDecreased(url,oldprice):
    url = unshorten_url(url)
    url = removeURLencoding(url)
    domain = find_domain(url)

    if domain== 'www.flipkart.com':
        newprice = flipkart_scrapper(url)
    elif domain== 'www.amazon.in':
        newprice = amazon_scrapper(url)
    elif domain== 'www.snapdeal.com':
        newprice = snapdeal_scrapper(url)
    else :
        raise NotImplementedError 

    print "newprice",newprice
    print "oldprice",oldprice
    if newprice < oldprice:
        return newprice
    else:
        return 0


#Set up twitter API data
#############################################################
parser = SafeConfigParser( )
parser.read('config.ini')

#read API data from 'config.ini'  file
api = twitter.Api(consumer_key = parser.get('twitter_API', 'consumer_key'),
                      consumer_secret = parser.get('twitter_API', 'consumer_secret'),
                      access_token_key = parser.get('twitter_API', 'access_token_key'),
                      access_token_secret = parser.get('twitter_API', 'access_token_secret'))

mongo_data = mongo_retrieve( )             