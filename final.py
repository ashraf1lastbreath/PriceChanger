import sys
import re
import requests
from bs4 import BeautifulSoup
import twitter
from pymongo import MongoClient
from ConfigParser import SafeConfigParser


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
            

#2. Scrap Data from website :
################################ 
def scrapper(url):
    print ""
    response = requests.get(url)
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

    return (price_txt)


#3. Post  Price Reduction Notification on Twitter :
########################################## 
def Tw_reduce_post(screen_name, price,  status_id ):
    status = api.PostUpdate( str("@"+screen_name) + "  Price of your item has reduced to  Rs. " +str(price),in_reply_to_status_id=str(status_id))
    print(status.text)
    print "Posted on Twitter"


#4. Compare price from Database and price from scrapper again:
####################################################### 
def isPriceDecreased(url,oldprice):
    newprice = scrapper(url)
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