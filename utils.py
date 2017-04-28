import httplib
import urlparse


#remove encoding etc appearing in url after '?' character 
def removeURLencoding(url):
   head, sep, tail = url.partition('?')
   return head

#extract domain name from url
def find_domain(url):
    return url.split("//")[-1].split("/")[0]

#prevent twitter from shortening the URL
def unshorten_url(url):
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc)
    h.request('HEAD', parsed.path)
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    else:
        return url