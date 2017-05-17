# About Trakila

Trakila is an easy to use tracking software, which can be used to track data from websites. 
The data can then be analyzed and worked around with according to one's own needs. 
Trakila also provides notifications to the users according to the logic provided by them.

As of now, Trakila is being used to track prices of items on popular Indian online shopping websites. 
It is a friendly and useful software which helps to track prices of items online,and notify users whenever the price of the item goes down on popular online shopping portals.

A user provides the url of the item whose price he wants to track online. As of now, Trakila accepts user URLs through Twitter only.
The user tweets @trakila the url of the item. Trakila fetches the price of the item, and tweets back the present price of the item to the user handle.
In the background Trakila continously keeps tracking the item for any fluctuations in price


### Objective :
Track prices of your wish list items, set price drop alerts, study price graph history.


### Design :
Built using Python language, Trakila uses the following packages / modules :

* BeautifulSoup4
* Requests
* SafeConfigParser
* Twitter Rest API
* Pymongo
* MongoDB Cloud
* MongoDB Compass
* BlockingScheduler
* Heroku PaaS

### Usage :

Tweet us the URL of the product you want to keep track of on popular e-shopping portals, and leave the rest to us. 
Wait and watch until we notify you by replying to your tweet when the price of the product goes down.


### Technical :

PriceChanger has the following Python files :

###### initial.py : 
* Fetch data from Twitter through Twitter API whenever @trakila is mentioned
* Read API data from 'config.ini'  file 
* Set up twitter API data from config file
* Fetch Twitter Data, Post to MongoDB
* Post Reply to Twitter Mentions

###### scrapper.py : Scrap the URL provided on Twitter to fetch data regarding the price of the item from following websites :

* Flipkart :

	* include http header fields for Requests 
	```
    headers =   {
   	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate, sdch, br', 
    'Accept-Language' : 'en-US,en;q=0.8',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'
    }
    ```
	* define encoding at response level itself
	```
    response.encoding = 'utf-8'
    ```
	* try to scrap data from metadata tag for Description or description on Flipkart page
	```
    desc= soup.find(attrs={'name':'Description'})
    ```
	* if Meta tag Description 'Content' is not found, try scrapping using Title metadata 'name : description'  on Flipkart page
	```
    item = soup.find('h1', attrs={'class': '_3eAQiD'}) 
    price_txt = int(desc.split("Rs. ")[1].split(" ")[0] )   
    ```

* Amazon :
	* include http header fields for Requests (similar to Flipkart)
	* define encoding at response level itself
	* try to scrap data from 'span' id': 'productTitle' on Amazon page
	```
      item = soup.find('span', attrs={'id': 'productTitle'}) 
      price = soup.find('span', attrs={'class': 'a-size-medium a-color-price'}) 
     ```
    * if not found, try to scrap from 'class': 'a-size-large a-spacing-none'
    ```
    item = soup.find('h1', attrs={'class': 'a-size-large a-spacing-none'})
    price = soup.find('span', attrs={'id': 'priceblock_ourprice'}) 
    ```
    * For some cases, where a range of price is mentioned, need to scrap only the first price
    ```
    try :
		price = soup.find('span', attrs={'id': 'priceblock_ourprice'}) 
	except :
		price = soup.find('span', attrs = {'class' : 'currencyINR'})
     ```
 * Snapdeal :
 	* relatively easier to scrap
	* include http header fields for Requests 
	* define encoding at response level itself
	* scrap item name and price directly from website 	

###### final.py :  
* Retrieve Data from MongoDb to fetch old price and tweet status id. 
* Scrap the old URL provided on Twitter to fetch the latest price of the item.
* Compare the two prices
* If price has reduced, post the reduced price of the product on user's earlier tweet.

###### bootstrap.py :

use Blocking Scheduler to run a cron job to run initial.py and final.py after regular intervals 

###### utils.py : 

* contains useful utility functions used. 
* Eg. :
	*  remove encoding etc appearing in url after '?' character 
	*  extract domain name from url
	*  prevent twitter from shortening the URL

######  requirements.txt :

contains all the dependencies that need to be installed on the environment to run Trakila. Use   ```   pip install -r requirements.txt ``` to install all the dependencies

######  ProcFile :
required for declaring what commands are run by Trakila's dynos on the Heroku platform. It follows the process model. Necessary to declare various process types, such as multiple types of workers, a singleton process like a clock, or a consumer of the Twitter streaming API

######   config.ini : 
contains all the configuration details for Twitter API and MongoDB Cloud

### Future Plans :
* target price by user
* price graph history
* facebook integration
* email integration
* SMS integration
* point based game board for highest winner



