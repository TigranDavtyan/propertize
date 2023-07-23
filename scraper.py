import asyncio
import logging
import random
import re
from datetime import datetime

import requests
import locations
from data_storage import db
from properties import *

logger = logging.getLogger('listamscraper')

class ListAmParser:
    class Category:
        id_dollar = re.compile(r'item\/(\d+)\".*?><img data-original=\"//s\.list\.am/g/\d+/\d+\.[jpgwebp]+\"><div class=\"p\">(\$?[\d,]+ ?[֏₽]?)')
        next_page = re.compile(r'</span> &nbsp; <a href="/category/\d+/(\d+)?.*">Next')

        def getItemIdPrices(page: str):
            return [[int(id), price.replace(',','').replace(' ','')] for id,price in ListAmParser.Category.id_dollar.findall(page)]

        def getNextPageId(page: str):
            match = ListAmParser.Category.next_page.search(page)
            if match:
                return match.group(1)
            return match

    class Item:
        dollar_price = re.compile(r'<span>\$(\d{1,3}(,\d{3})*(\.\d+)?)')
        dram_price = re.compile(r'<span>([\d,]+)\s*֏')
        ruble_price = re.compile(r'<span>([\d,]+)\s*₽')

        house_props = re.compile(r'<div class="c">(?:<div class="t">(?P<key>.*?)<\/div>)?<div class="i">(?P<value>.*?)<\/div><\/div>')

        posted_dt = re.compile(r'Posted (\d{2}\.\d{2}\.\d{4})')
        renewed_dt = re.compile(r'Renewed (\d{2}\.\d{2}\.\d{4})')

        address = re.compile(r'title="Show the map" onclick="dlgo\(\'(.+?)\',\s*\'\/\?w=11&i=\d+&m=\d+\'')
        address2 = re.compile(r"onclick=\"dlgo\('(.+),\s*([\w\s]+)'\s*,\s*'/\?w=.*'\s*,\s*\d+\);return false;\">(.+)</a>")

        user = re.compile(r'<a href="/user/(\d+)" class')

        def getUser(page: str):
            userid = ListAmParser.Item.user.search(page)
            if userid:
                userid = userid.group(1)
            return userid
        
        def getPrices(page: str):
            dollar_price,dram_price,ruble_price = None,None,None
            dollar_price = ListAmParser.Item.dollar_price.search(page)
            if dollar_price: dollar_price = dollar_price.group(1)
            dram_price   = ListAmParser.Item.dram_price.search(page)
            if dram_price: dram_price = dram_price.group(1)
            ruble_price  = ListAmParser.Item.ruble_price.search(page)
            if ruble_price: ruble_price = ruble_price.group(1)
            
            return [dollar_price, dram_price, ruble_price]
        
        def getDatetimes(page: str):
            posted_match = ListAmParser.Item.posted_dt.search(page)
            renewed_match = ListAmParser.Item.renewed_dt.search(page)
            posted_date, renewed_date = None, None
            if posted_match:
                posted_date = posted_match.group(1)
                posted_date = datetime.strptime(posted_date, '%d.%m.%Y').date()

            if renewed_match:
                renewed_date = renewed_match.group(1)
                renewed_date = datetime.strptime(renewed_date, '%d.%m.%Y').date()
            else: renewed_date = posted_date

            return [posted_date,renewed_date]
        
        def getAddress(page: str):
            match = ListAmParser.Item.address.search(page)
            address = match.group(1)

            city, street= None, None

            if address.find(',') > -1:
                street, city = address.split(',')
            elif address.find('›') > -1:
                city = address.split('›')[1].replace(' ','')
                
            return [city, street]

        def getHouse(page: str):
            # Extract item properties as dictionary
            properties = dict(ListAmParser.Item.house_props.findall(page, re.DOTALL | re.IGNORECASE))
            properties = {k.lower().replace(' ', '_'): v.lower().replace(' ', '_') for k, v in properties.items() if v}

            try:
                userid = ListAmParser.Item.getUser(page)
                properties['userid'] = userid
            except:
                pass

            try:
                prices = ListAmParser.Item.getPrices(page)
                properties['dollar_price'] = prices[0]
                properties['dram_price'] = prices[1]
                properties['ruble_price'] = prices[2]
            except:
                pass

            try:
                dts = ListAmParser.Item.getDatetimes(page)
                properties['posted_date'] = dts[0]
                properties['update_date'] = dts[1]
            except:
                pass
            
            try:
                city, street = ListAmParser.Item.getAddress(page)
                properties['city'] = city
                properties['street'] = street
            except:
                pass

            for key, value in properties.items():
                properties[key] = HouseProperties.get(key,value)

            properties['closed_item'] = 0

            return properties
        

class Category:
    def __init__(self, categoryid, url, name, monthly_or_daily = 0):
        self.categoryid = categoryid
        self.item_url = 'https://www.list.am/en/item/{itemid}'
        self.url = url
        self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'}
        self.itemids = []
        self.name = name
        self.monthly_or_daily = monthly_or_daily

        self.new = 0
        self.updated = 0
        self.same = 0
        self.error = 0
        self.no_price = 0
        self.closed = 0

    async def sleepRandom(self):
        await asyncio.sleep(random.random()*0.8 + 0.5)

    def getUrl(self, location_id, page = None):
        if not page or page < 2:
            pagestr = ''
        else: pagestr = page

        page_url = self.url.format(id=self.categoryid, page=pagestr, monthly_or_daily = self.monthly_or_daily, location_id = location_id)

        logger.debug(page_url)
        response = requests.get(page_url, headers=self.headers)
        if response.status_code != 200:
            logger.error(f'Response code {response.status_code}')
            return response.status_code
        return response.content.decode('utf-8')
       
    def getItem(self, itemid):
        url = self.item_url.format(itemid = itemid)

        logger.debug(url)
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            logger.error(f'Response code for {response.status_code} for {url}')
            return response.status_code
        return response.content.decode('utf-8')
    
    async def getItemIds(self, location_id, limit=None):
        next = 1
        while True:
            page = self.getUrl(location_id, next)
            if not page:
                next += 1
                continue

            idprices = ListAmParser.Category.getItemIdPrices(page)
            for idprice in idprices:
                item = {}
                item['original_price'] = 0
                #$֏₽
                if '$' in idprice[1]:
                    item['dollar_price'] = int(idprice[1].replace('$',''))
                    item['original_price'] = item['dollar_price']
                elif '֏' in idprice[1]:
                    item['dram_price'] = int(idprice[1].replace('֏',''))
                    item['original_price'] = item['dram_price']
                elif '₽' in idprice[1]:
                    item['ruble_price'] = int(idprice[1].replace('₽',''))
                    item['original_price'] = item['ruble_price']

                item['itemid'] = idprice[0]
                item['location'] = location_id
                item['monthly_or_daily'] = self.monthly_or_daily
                self.itemids.append(item)

            if limit and len(self.itemids) > limit:
                self.itemids = self.itemids[:limit]
                break

            next = ListAmParser.Category.getNextPageId(page)

            if not next:
                break
            next = int(next)
            
            await self.sleepRandom()

        self.itemids = list({item['itemid']:item for item in self.itemids}.values())

    async def getItems(self):
        db.createBackup()
        #if there is an item id which exists in db but not in the newly scraped list we flag them as finished
        existing_ids = set([d[0] for d in db.fetchall('SELECT itemid FROM listings WHERE website = "list.am" AND closed_item=0 AND categoryid = ? AND monthly_or_daily=?;',(self.categoryid, self.monthly_or_daily))])
        new_ids = set([item['itemid'] for item in self.itemids])
        
        for itemid in existing_ids.difference(new_ids):
            db.closeItem(itemid)
            self.closed += 1
        del new_ids
        del existing_ids
        ###

        percent_modulo = int(len(self.itemids)/100)
        percent_modulo = 1 if percent_modulo == 0 else percent_modulo
        
        for i,item in enumerate(self.itemids):
            if i % percent_modulo == 0:
                logger.info(f'Processed {round(i/len(self.itemids)*100)}% of {len(self.itemids)} items. Same {self.same} | New {self.new} |  Updated {self.updated} |  Error {self.error} | No price {self.no_price} | Closed {self.closed}')
            
            if self.error > 20 and self.error/(self.updated+self.same+self.no_price+1)*100 > 8:
                logger.error('Stopping scraping because too many error')
                db.restoreBackup()
                return False

            if item['original_price'] == 0: #Passing items which dont have a price
                self.no_price += 1
                continue

            op = db.fetchone('SELECT original_price FROM listings WHERE itemid = ?;',(item['itemid'],))
            if op and op[0] == item['original_price']: #Passing items which are the same
                self.same += 1
                continue
            
            try:
                page = self.getItem(item['itemid'])
                item['itemid'] = item['itemid']
                if page:
                    properties = ListAmParser.Item.getHouse(page)
                    properties['categoryid'] = self.categoryid
                    properties['website'] = 'list.am'
                    properties.update(item)

                    ret = db.insertOrUpdateListing(properties)
                    if ret == 0:
                        self.same += 1
                    elif ret == 1:
                        self.updated += 1
                    elif ret == 2:
                        self.new += 1
                elif page == 404:
                    db.closeItem(item['itemid'])
                    self.closed += 1
                else:
                    raise ValueError('status code '+str(page))
                
            except Exception as e:
                logger.debug(f'{item["itemid"]} passed  '+ str(e))
                await asyncio.sleep(1)

                self.error += 1
                continue

            logger.debug(properties)
            del properties

            await self.sleepRandom()

        logger.info(f'ListAm {self.name} : Same {self.same} | New {self.new} |  Updated {self.updated} |  Error {self.error} | No price {self.no_price} | Closed {self.closed}')
        return True
    
    async def update_data(self, location_group: locations.LocationGroup, limit = None):
        logger.info(f"STARTING TO SCRAPE LIST AM {self.name}")

        logger.info('Getting item ids...')
        for i, location_id in enumerate(list(location_group.values())):
            await self.getItemIds(location_id, limit)

        logger.info(f'Found {len(self.itemids)} listings')
        
        logger.info('Getting items...')
        try:
            await self.getItems()
        except Exception as e:
            logger.error('Stopping scraping because too many error ' + str(e))
            db.restoreBackup()
        
        logger.info(f"FINISHED SCRAPING LIST AM {self.name}")


class ForRent:
    url = 'https://www.list.am/en/category/{id}/{page}?pfreq={monthly_or_daily}&type=1&n={location_id}&price1=&price2=&crc=-1&_a5=0&_a39=0&_a40=0&_a3_1=&_a3_2=&_a4=0&_a37=0&_a11_1=&_a11_2=&_a78=0&_a38=0&_a68=0&_a69=0'
    
    properties = HouseProperties
    
    DEFAULT = 0
    MONTHLY = 1
    DAILY = 2
    
class Monthly:
    Apartments = Category(56, ForRent.url, 'ForRent Apartments monthly',ForRent.MONTHLY)
    Houses = Category(63, ForRent.url, 'ForRent Houses monthly',ForRent.MONTHLY)
    Rooms = Category(212, ForRent.url, 'ForRent Rooms monthly',ForRent.MONTHLY)
    CommercialHouseProperties = Category(59, ForRent.url, 'ForRent CommercialHouseProperties monthly',ForRent.MONTHLY)
    EventVenues = Category(267, ForRent.url, 'ForRent EventVenues monthly',ForRent.MONTHLY)
    GaragesandParking = Category(175, ForRent.url, 'ForRent GaragesandParking monthly',ForRent.MONTHLY)
    TrailersandBooths = Category(58, ForRent.url, 'ForRent TrailersandBooths monthly',ForRent.MONTHLY)

class Daily:
    Apartments = Category(56, ForRent.url, 'ForRent Apartments daily',ForRent.DAILY)
    Houses = Category(63, ForRent.url, 'ForRent Houses daily',ForRent.DAILY)
    Rooms = Category(212, ForRent.url, 'ForRent Rooms daily',ForRent.DAILY)
    CommercialHouseProperties = Category(59, ForRent.url, 'ForRent CommercialHouseProperties daily',ForRent.DAILY)
    EventVenues = Category(267, ForRent.url, 'ForRent EventVenues daily',ForRent.DAILY)
    GaragesandParking = Category(175, ForRent.url, 'ForRent GaragesandParking daily',ForRent.DAILY)
    TrailersandBooths = Category(58, ForRent.url, 'ForRent TrailersandBooths daily',ForRent.DAILY)
    
class ForSale:
    url = 'https://www.list.am/en/category/{id}/{page}?type=1&n={location_id}&price1=&price2=&crc=-1&_a5=0&_a39=0&_a40=0&_a3_1=&_a3_2=&_a4=0&_a37=0&_a11_1=&_a11_2=&_a78=0&_a38=0'

    properties = HouseProperties

    Apartments = Category(60, url, 'ForSale Apartments')
    Houses = Category(62, url, 'ForSale Houses')
    Land = Category(55, url, 'ForSale Land')
    CommercialHouseProperties = Category(199, url, 'ForSale CommercialHouseProperties')
    GaragesandParking = Category(173, url, 'ForSale GaragesandParking')
    TrailersandBooths = Category(61, url, 'ForSale TrailersandBooths')