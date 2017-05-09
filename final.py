# -*- coding: utf-8 -*-

import twitter
#import requests
from pymongo import MongoClient
from ConfigParser import SafeConfigParser
import sys
from scrapper import flipkart_scrapper, amazon_scrapper, snapdeal_scrapper
from utils import  removeURLencoding, find_domain, unshorten_url


#1. Retrieve Data from MongoDb :
################################ 
def mongo_retrieve( api):
    parser = SafeConfigParser( )
    parser.read('config.ini')

    connection = MongoClient(parser.get('mongo_server', 'mongo_url'))
    db = connection.pricechanger.message

    results = db.find({'is_replied': False})
    print " "
    print " Fetching Data from MongoDb :"
    print "==========================="
    for record in results:
        print record
        newprice = isPriceDecreased(record['url'],record['price'])
        if newprice > 0:
            Tw_reduce_post(api, record['screen_name'], newprice, record['status_id'], record['item'])
            db.find_one_and_update(
                {'_id': record['_id']},
                {'$set': {'is_replied': True}}
            )
            

#3. Post  Price Reduction Notification on Twitter :
########################################## 
def Tw_reduce_post(api, screen_name, price,  status_id , item):
    status = api.PostUpdate( str("@"+screen_name) + "  Price of " + item[:80] + " has reduced to Rs. " +str(price),in_reply_to_status_id=str(status_id))
    print(status.text)
    print "Notified user about reduced price on Twitter"


#4. Compare price from Database and price from scrapper again:
####################################################### 
def isPriceDecreased(url,oldprice):
    url = unshorten_url(url)
    url = removeURLencoding(url)
    domain = find_domain(url)

    try:
        url = unshorten_url(url)
        url = removeURLencoding(url)
        domain = find_domain(url)

        if domain== 'www.flipkart.com':
            scrapped = flipkart_scrapper(url) 
            newprice = scrapped[0]

        elif domain== 'www.amazon.in':
            scrapped = amazon_scrapper(url)
            newprice = scrapped[0]

        elif domain== 'www.snapdeal.com':
            scrapped = snapdeal_scrapper(url)
            newprice = scrapped[0]

        else :
            raise NotImplementedError ("This domain is not supported yet in our system. Be back Later !")

    except :
        print "Unable to fetch new price from website. Will try again later."
        sys.stdout.flush()    

    print "newprice",newprice
    print "oldprice",oldprice
    if newprice < oldprice:
        return newprice
    else:
        return 0


#Set up twitter API data
#############################################################
def final( ):
    parser = SafeConfigParser( )
    parser.read('config.ini')

    #read API data from 'config.ini'  file
    api = twitter.Api(consumer_key = parser.get('twitter_API', 'consumer_key'),
        consumer_secret = parser.get('twitter_API', 'consumer_secret'),
        access_token_key = parser.get('twitter_API', 'access_token_key'),
        access_token_secret = parser.get('twitter_API', 'access_token_secret'))
    
    mongo_retrieve(api )   

'''
parser = SafeConfigParser( )
parser.read('config.ini')

#read API data from 'config.ini'  file
api = twitter.Api(consumer_key = parser.get('twitter_API', 'consumer_key'),
        consumer_secret = parser.get('twitter_API', 'consumer_secret'),
        access_token_key = parser.get('twitter_API', 'access_token_key'),
        access_token_secret = parser.get('twitter_API', 'access_token_secret'))

mongo_data = mongo_retrieve(api )   '''

