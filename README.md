

[![](http://icons.iconarchive.com/icons/graphics-vibe/simple-rounded-social/128/twitter-icon.png)](https://twitter.com/Price_Changer)
# PriceChanger  
##### Powered by Twitter
-------------------

PriceChanger is a friendly and useful app built using Python Language, powered by  Twitter DevTools, which helps to notify users whenever the price of the item goes down on popular online shopping portals like Flipkart, Amazon and SnapDeal.

Built using Python language, it uses the following Python packages / modules :
  - BeautifulSoup4
  - Requests
  - Twitter
  - Pymongo 
  - SafeConfigParser

#  Features!

  - Tweet us the URL of the product you want to keep track of on popular e-shopping portals, and leave the rest to us. Wait and watch until we notify you by replying to your tweet when the price of the product goes down.
  - Supports only Flipkart portal as of now. Will be working to add other popular ecommerce sites very soon.


### Tech

PriceChanger has the following Python files :

* [scrapper.py] - It performs following operations :
    * Fetch data from Twitter through Twitter API whenever Price_Changer is mentioned
    *  Scrap the URL provided on Twitter to fetch data regarding the price of the item
    *  Post the data to MongoDb
    *  Post the initial price of the product on user's tweet

* [droid.py] - It performs following operations :
    * Retrieve Data from MongoDb to fetch old price and tweet status id
    *  Scrap the old URL provided on Twitter to fetch the latest price of the item
    *  Compare the two prices
    *  If price has reduced, post the reduced price of the product on user's earlier tweet.
    

### Installation

PriceChanger requires following dependencies to run.
  - BeautifulSoup4
  - Requests
  - Twitter
  - Pymongo 
  - SafeConfigParser
  
To install the dependencies and devDependencies and start the server, simply typ ethe following on the command prompt, before starting the programs :

```sh
$ pip install -r requirements.txt
```



### Usage
 - Run both the python files using a cronjob on a server 
  - On Twitter simply post the URL of any product from any popular ecommerece sites, and tweet it to @Price_Changer'
                   @Price_Changer space URL    

#License

##Ashraf

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
