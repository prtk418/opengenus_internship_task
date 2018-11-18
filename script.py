import sys
import urllib2
from urlparse import urlparse
import BeautifulSoup
import requests
import humanfriendly

def get_domain_name(url):
    uri_parsed = urlparse(url)
    return '.'.join(((uri_parsed.hostname).split('.')[1:]))

def get_url_response(url):
    request = urllib2.Request(url)
    return urllib2.urlopen(request)

def count_links(url,domain):
    response = get_url_response(url)
    soup = BeautifulSoup.BeautifulSoup(response)
    count = 0
    for a in soup.findAll('a', href=True):
        if domain in a['href']:
            count += 1
    if response:
        response.close()
    return count

def get_page_size(response):
    response = get_url_response(url)
    size = len(response.read())
    if response:
        response.close()
    return size

# If no arguments passed
if len (sys.argv) < 2 :
    print "Please enter atleast one url"
    sys.exit (1)

# Extract urls from input
urls = sys.argv[1:]

# Iterate over input urls
for i,url in enumerate(urls):
    # Skip if bad url
    try:
         data = urllib2.urlopen(url)
    except:
         print("URL{} =>\nInvalid URL\n".format(i+1))
    else:
        result = {}
        webpage_size_raw = get_page_size(url)
        result['webpage_size'] = humanfriendly.format_size(webpage_size_raw)
        domain_name = get_domain_name(url)
        result['num_links'] = count_links(url,domain_name)

        print("\nURL{} =>\n{}\n".format(i+1,result))
