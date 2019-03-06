import requests
from lxml import html

site_url = 'https://eresearch.fidelity.com/eresearch/gotoBL/fidelityTopOrders.jhtml'

def start_scraping():
    response = requests.get(site_url)
    sourceHtml = response.text

    print('source html', sourceHtml)

if (__name__ == '__main__'):
    start_scraping()