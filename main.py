import logging
import datetime
import sys
import time
import os
import platform

import locations
from scraper import ForRent, ForSale
import asyncio
from data_storage import db

def log_exceptions(exctype, value, traceback):
    logger = logging.getLogger('listamscraper')
    logger.error(exctype, value, traceback)
    sys.__excepthook__(exctype, value, traceback)

sys.excepthook = log_exceptions

async def run():
    logger = logging.getLogger('listamscraper')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('listamscraper.log','a', 'utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info("START TO SCRAPE")

    for i, location_id in enumerate(list(locations.YEREVAN.values())):
        await ForRent.Apartments.update_data(location_id, ForRent.MONTHLY)
        await ForRent.Apartments.update_data(location_id, ForRent.DAILY)
        await ForRent.Houses.update_data(location_id, ForRent.MONTHLY)
        await ForRent.Houses.update_data(location_id, ForRent.DAILY)

        await ForSale.Apartments.update_data(location_id)
        await ForSale.Houses.update_data(location_id)

    logger.info("UPDATING GOOGLE SHEET")
    ret = db.updateSheet()
    # logger.info(f'Updated {ret.} rows on google sheet')
    logger.info("FINISHED SCRAPING")
    
    
async def main():
    if platform.system() in ['Linux', 'Darwin']:
        os.environ['TZ'] = 'Asia/Yerevan'
        time.tzset()

    if len(sys.argv) == 2:
        run_time = time.strptime(sys.argv[1], '%H:%M')
        now = datetime.datetime.now()
        next_run = now.replace(hour=run_time.tm_hour, minute=run_time.tm_min, second=0)
        if next_run < now:
            next_run += datetime.timedelta(days=1)
        wait_time = (next_run - now).total_seconds()-1
        print('Next run',next_run,'   wait time ', wait_time,'(seconds)')
    else:
        print('No time parameter. You should give a time parameter like this main.py 8:00 or it will run asap')
        next_run = datetime.datetime.now()
        wait_time = 0

    while True:
        time.sleep(wait_time)

        await run()

        now = datetime.datetime.now()
        next_run += datetime.timedelta(days=1)
        wait_time = (next_run - now).total_seconds()
        print('Next run', next_run,'   wait time ', wait_time,'(seconds)')


if __name__ == '__main__':
    asyncio.run(main())