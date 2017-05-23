#!/usr/bin/python
import mechanize
from bs4 import BeautifulSoup

def scrape_links(base_url, data):
  # Create mechanize links to be used later by mechanize.Browser instance
  soup = BeautifulSoup(data, 'html.parser')
  '''base_url = base_url
  anchor = { }
  #url = str(anchor['href'])
  text = str(anchor.string)
  tag = str(anchor.name)
  attrs = [(str(name), str(value))]
  print base_url, ur, text, tag, attrs'''
  #for name, value in anchor.attrs


  links = [mechanize.Link (base_url = base_url, 
  url = str(anchor['href']),
  text = str(anchor.string),
  tag = str(anchor.name),
  attrs = [(str(name), str(value))
  for name, value in anchor.attrs])
  for anchor in soup.packt-article-line-view-title.findAll("div")]






def main( ):
  #Get item network main page and follow the links to get the whole list of description available
  items = ""
  # Get main page and get links to all item pages
  url = "https://www.flipkart.com/crocs-girls/p/itmemyhfshgz2zm8?pid=SHOEMYXDPKN3YJ55&srno=b_1_1&otracker=hp_omu_Deals%20of%20the%20Day_1_50-80%25%20Off_f25e91f9-d8c9-471d-92cd-658265333098&lid=LSTSHOEMYXDPKN3YJ55VC3AOW"
  #url = "http://www.packtpub.com/article-network"
  br = mechanize.Browser( )
  response = br.open(url)
  response = br.open(url)
  #print response.read()      # the text of the page
  response1 = br.response()  # get the response again
  #print response1.read()     # can apply lxml.html.fromstring()

  #display forms used
  for form in br.forms():
    print "Form name:", form.name
    print form


  '''data = br.open(url).get_data()
  links = scrape_links(url, data)
  browser.open(url)
  print "links :", links'''

if __name__ == "__main__":
    main( )



