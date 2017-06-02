# -*- coding: utf-8 -*-

import requests
import sys
from bs4 import BeautifulSoup
import re
import logging
import html2text
from bs4 import BeautifulSoup as BSHTML
logging.basicConfig( )

#Scrap URL to fetch data
########################

#############################FLIPKART scrapper##########################################
########################################################################################
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

    #RETRIEVE ITEM NAME
    ####################################################
    search_str_item = "_3eAQiD"     # add more search strings here
    item = soup.select("h1[class^="+str(search_str_item)+"]")
    if item== None :
        try :
            # Case 1 : If Search String of Item is not found, try to extract  Item Namefrom Meta Data
            item_txt = str(desc.split("Buy ")[1].split("Rs. " )[0] )  #if not found, try scrapping using Title metadata name : description  
            print "Debug 1 : Item found:", str(item_txt)
            found = True
        except:
            # Case 2: Failed case : send Item Name as empty string
            item_txt = " "
            found = False
            print "Error 2 : Product not found"
    else :
        try :
            # Case 3 : If Search String of Item is found, extract only text part from Item HTML 
            h = html2text.HTML2Text()
            h.ignore_links = True  # Ignore converting links from HTML

            #to retrieve the text from html obtained
            item_txt = h.handle(str(item))   
            item_txt = html2text.html2text(item_txt)   #to remove html parts
            item_txt = " ".join(item_txt.split())              #to remove extra spaces
            item_txt = item_txt[4:-1]                               #to select text between string array obtained

            print "Debug 3 : item_txt  found : ", str(item_txt)    
            found = True
        except :
            # Case 4:  If Search String of Item is found, and HTML2Text doesnt work, extract item name manually from Item HTML
            BS = BSHTML(str(item),'html.parser')
            result = re.compile(' -->(.*?)<!-- ')
            item = result.search(str(BS))

            if item:
                item = item.group(1)
                item_txt = re.sub(' +',' ',item)        #remove extra white spaces
            print "Debug 4 : item_txt  found :", str(item_txt)        
            found = True



     #RETRIEVE  PRICE
    ####################################################
    search_str_price = "_1vC4OE"
    price = soup.select("div[class^="+str(search_str_price)+"]")
    price = price[0]              #select first of multiple tags selected
    #print "price :",price
    if price== None :     
        # Case 1 : If Search String of Price is not found, try to extract  Price from Meta Data       
       try :
                desc= soup.find(attrs={'name':'Description'})
                try:
                    #print desc['content']
                    desc =  desc['content']
                except :
                    print "Meta tag Description 'Content' not found"
                price_txt = int(desc.split("Rs. ")[1].split(" ")[0] )                #if not found, try scrapping using Title metadata name : description 
                print "Debug 1 : Price found :",str(price_txt)
                found = True

        # Case 2: Failed case : send Price as neg num
       except :
                price_txt = -1
                found = False
                print "Error 2 : Price not found"
                pass
    else :
        try :
                #CASE 3 :   If Search String of Price is found, extract only text part from Price HTML
                h = html2text.HTML2Text()
                h.ignore_links = True  # Ignore converting links from HTML
      
                price_txt = h.handle(str(price))                      #to retrieve the text from html obtained
                price_txt = re.sub("[^0-9]", "",price_txt )      #Removing Non Numeric symbols from Price
                price_txt  = int(price_txt[3:])                                   #Remove the digits left behind by Rupee symbol
                print "Debug 3 : Price found :",str(price_txt)    
                found = True

        except :            
                # CASE 4:  If Search String of Price is found, and HTML2Text doesnt work, extract price manually from price HTML     
                 result = re.findall(" -->(.*?)<!-- ",str(price))    # find all items between --> and <-- in price
                 price_txt =  result[2]                                            # price is the third occurance in the search array
                 price_txt = re.sub("[^0-9]", "",price_txt )        #Removing Non Numeric symbols from Price
                 print "Debug 4: price_txt  found :", str(price_txt)        
                 found = True


    print  "Present price  of  " + str(item_txt ) + " on Flipkart is Rs. " + str(price_txt)
    print "----------------------------------------------------------------------------------------------------------------"
    print ""
    return (price_txt, item_txt, found)




#############################Amazon . IN scrapper##########################################
#########################################################################################
def amazon_scrapper(url):
    import sys
    reload(sys)  
    sys.setdefaultencoding('Cp1252')

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
    reload(sys)  
    sys.setdefaultencoding('Cp1252')
    html = response.content            #fetch the entire HTML of the URL
    
    
    soup = BeautifulSoup(html,'html.parser')
    found = False

    h = html2text.HTML2Text()
    h.ignore_links = True  # Ignore converting links from HTML


    #RETRIEVE ITEM NAME
    ####################################################
    search_str_item = "a-size-large"     # add more search strings here
    reload(sys)  
    sys.setdefaultencoding('Cp1252')
    item = soup.select("span[class^="+str(search_str_item)+"]")
    if not item :
        print "Encoding problem encountered...Retrying ..."
        reload(sys)  
        sys.setdefaultencoding('Cp1252')
        item = soup.select("span[class^="+str(search_str_item)+"]")  

    if not item :
        try :         
            # Case 1 : If Search String of Item is not found, try to reload sys and try again
            import time
            time.sleep(10)
            reload(sys)  
            sys.setdefaultencoding('Cp1252')

            item = soup.select("span[class^="+str(search_str_item)+"]")
            item_txt = h.handle(str(item))
            print "Debug 1 : Item found:", str(item_txt)
            found = True
        except:
            # Case 2: Failed case : send Item Name as empty string
            item_txt = " "
            found = False
            print "Error 2 : Product not found"
    else :
        try :
            # Case 3 : If Search String of Item is found, extract only text part from Item HTML 
            reload(sys)  
            sys.setdefaultencoding('Cp1252')

            #to retrieve the text from html obtained
            item_txt = h.handle(str(item))   
            #item_txt = h.aandle(str(item))   # aandle to forcibly go to Debug 3
            item_txt = html2text.html2text(item_txt)   #to remove html parts
            item_txt = " ".join(item_txt.split())              #to remove extra spaces
            item_txt = item_txt[15:-10]                               #to remove new line characters /n

            print "Debug 3 : item_txt  found : ", str(item_txt)    
            found = True

        except :
            # Case 2:  If Search String of Item is found, and HTML2Text doesnt work, extract item name manually from Item HTML
            reload(sys)  
            sys.setdefaultencoding('Cp1252')

            BS = BSHTML(str(item),'html.parser')
            BS = str(BS)[1:-1]                          # remove array square brackets
            BS = ''.join(str(BS).split())           # remove extra spaces
            BS = str(BS).replace("\\n", "")   # remove new line characters

            result = re.compile('>(.*?)</')    #select text between > and < tags
            item = result.search(str(BS))

            if item:
                item = item.group(1)
                item_txt = re.sub(' +',' ',item)        #remove extra white spaces
            print "Debug 4 : item_txt  found :", str(item_txt)        
            found = True



    #RETRIEVE  PRICE
    ####################################################
    search_str_price = "a-size-medium a-color-price"
    price = soup.select('span[class^="'+str(search_str_price)+'"]')
    #eg.   : soup.select('a[href^="http://example.com/"]')
    price = price[0]    # select first one if multiple tags are selected

    #To handle price ranges in Amazon
    if '- <' in str(price) :
        print "Range of Price Detected. Selecting the first price only"
        price_copy = price
        price = None

    if price== None :     
        try:
            #For a range of Price block
            start = "<span "
            end = "00 - "
            price = re.findall('<span (.*?) - ',str(price_copy))
            price = re.sub("[^0-9]", "",str(price) )         #Removing Non Numeric symbols from Price
            price = price [4:]                                              #remove digits left behind by Rupee symbol
            price_txt = int(price) / 100                             #remove digits left behind by decimal symbol

            found = True
            print "Debug 1 : Price found :" + str(price_txt)     

        # Case 2: Failed case : send Price as neg num
        except :
                price_txt = -1
                found = False
                print "Error 2 : Price not found"
                pass
    else :
        try :
                #CASE 3 :   If Search String of Price is found, extract only text part from Price HTML
                h = html2text.HTML2Text()
                h.ignore_links = True  # Ignore converting links from HTML
      
                price_txt = h.handle(str(price))                               #to retrieve the text from html obtained
                price_txt = re.sub("[^0-9]", "",price_txt )                #Removing Non Numeric symbols from Price
                price_txt = int(price_txt ) / 100                                  #Remove the digits left behind by decimal point
                print "Debug 3 : Price found :",str(price_txt)    
                found = True

        except :            
                # CASE 4:  If Search String of Price is found, and HTML2Text doesnt work, extract price manually from price HTML     
                 price = re.sub("[^0-9]", "",str(price) )                     #Removing Non Numeric symbols from Price
                 price_txt = int(price) /100                                           # Remove zeroes left behind by decimal point
                 print "Debug 4: price_txt  found :", str(price_txt)        
                 found = True


    print  "Present price  of  " + str(item_txt ) + " on Amazon is Rs. " + str(price_txt)
    print "----------------------------------------------------------------------------------------------------------------"
    print ""
    return (price_txt, item_txt, found)



#############################SNAPDEAL scrapper########################################
########################################################################################
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
         item_txt = str(item_txt.encode('utf-8').strip() )         # to remove trailing and leading whitespaces
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
    print "----------------------------------------------------------------------------------------------------------------"
    print ""
    return (price_txt, item_txt, found )
