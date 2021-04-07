import requests
from bs4 import BeautifulSoup
import time
from twilio.rest import Client
import urllib.request
from multiprocessing import Pool

client = Client('', '')

def tiny_url(url):
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.request.urlopen(apiurl + url).read()
    return tinyurl.decode("utf-8")

def check(url):
    while True:
        response = requests.get(url)
        html = BeautifulSoup(response.text, 'html.parser')

        if str(html).find('<span>Add to Cart</span>') != -1:
            # Message information
            title = str(html.title)
            title = title[7:title.index('|')-1]
            message = client.messages.create(
                                body=("Item Available: " + title + "\n\nLink: " + tiny_url(url)),
                                from_='+twilio-number',
                                to='+your-number')
            
            print('Item Found: ' + title + '\nMessage SID: ' + message.sid)
            break

        else:
            print('No item found, waiting 5 minutes.')
            time.sleep(300)

if __name__ == '__main__':
    with Pool(3) as p:
        urls = ['https://www.roguefitness.com/rogue-ohio-bar-black-oxide', 
                'https://www.roguefitness.com/the-ohio-bar-black-zinc',
                'https://www.roguefitness.com/the-ohio-bar-2-0-e-coat']
        p.map(check, urls)
