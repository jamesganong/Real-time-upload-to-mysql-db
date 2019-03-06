import requests
from lxml import html
import pymysql.cursors
import time
from apscheduler.schedulers.blocking import BlockingScheduler

def store_on_mysql_database(scraped_data):
    print('stroing on mysql databse...')
    timestamp = time.ctime(time.time())

    # Connect to the database
    connection = pymysql.connect(host='localhost',
        user='admin',
        password='',
        db='test',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    try:
        for row in scraped_data:
            rank, symbol, company, priceChange, buyOrder, sellOrder, news = row

            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `stock_research` \
                    (`rank`, `symbol`, `company`, `priceChange`, `buyOrder`, `sellOrder`, `newLink`, `timestamp`) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

                cursor.execute(sql, (rank, symbol, company, priceChange, buyOrder, sellOrder, news, timestamp))

            connection.commit()

        ###############################################################
        #NOTE: Tip for you....
        #You can run this command to see all data is stored correctly
        ###############################################################
        # with connection.cursor() as cursor:
        #     # Read a single record
        #     sql = "SELECT company FROM `stock_research`"
        #     cursor.execute(sql)
        #     result = cursor.fetchone()
        #     print(result)
    finally:
        connection.close()

    print('completed!')

def start_scraping():
    site_url = 'https://eresearch.fidelity.com/eresearch/gotoBL/fidelityTopOrders.jhtml'
    base_url = 'https://eresearch.fidelity.com'

    # NOTE: Load the web page
    print('feching the page...')
    response = requests.get(site_url)
    page = html.fromstring(response.text)

    # NOTE: Extract data from fetched page
    rowsData = page.xpath('//table[@id="topOrdersTable"]/tbody//tr')

    scraped_data = []
    for row in rowsData:
        rank = row.xpath('.//td[@class="first"]/text()')[0]
        symbol =  row.xpath('.//td[@class="second"]/span/@fmr-param-symbol')[0]
        company = row.xpath('.//td[@class="third"]/text()')[0]
        priceChange = row.xpath('.//td[contains(@class, "fourth")]/text()')[0]
        buyOrder = row.xpath('.//td[@class="fifth"]/text()')[0]
        sellOrder = row.xpath('.//td[@class="seventh"]/text()')[0]
        news = row.xpath('.//td[contains(@class, "eight")]/span/a/@href')[0]

        scraped_data.append((
            rank, symbol, company, priceChange, buyOrder, sellOrder, base_url+news
        ))

    print('^^^scraped data is as below^^^')
    for row in scraped_data:
       rank, symbol, company, priceChange, buyOrder, sellOrder, news = row
       print(rank, symbol, company, priceChange, buyOrder, sellOrder, news)

    #NOTE: store the result on mysql server
    store_on_mysql_database(scraped_data)

if (__name__ == '__main__'):
    start_scraping()

    scheduler = BlockingScheduler()
    scheduler.add_job(start_scraping, 'interval', minutes=1)
    scheduler.start()