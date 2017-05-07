from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import os, platform
import threading
import time
import importlib
import random
import re
import json
import pprint
import storage
import my_threading
import my_driver
import urllib



by_mapper = {
    "class": By.CLASS_NAME,
    "tag": By.TAG_NAME,
    "id": By.ID,
    "attr": "attr",
    "text": "text"
}


class Crawler(object):

    def __init__(self):
        pass
        # threading.Thread.__init__(self)

    def crawl(self, url):
        self.url = url
        self.b = my_driver.get_driver(platform.system())
        self.run()

    def run(self):
        rand = random.randint(2, 10)
        time.sleep(rand)
        url = self.url
        print('crawl: %s' % url)
        b = self.b

        b.get(url)
        scripts = b.find_elements_by_tag_name('script')
        time.sleep(2)

        def find_until(until, _script):
            if until <= 0:
                return ""
            time.sleep(3)
            try:
                innerHTML = _script.get_attribute('innerHTML')
                return innerHTML
            except Exception:
                return find_until(until-1, _script)

        for script in scripts:
            try:
                innerHTML = find_until(3, script)
            except:
                print(self.url)
                continue

            if "dabang.web.detail" not in innerHTML:
                continue

            my_json = re.findall(r'dabang.web.detail\((.*)\);', innerHTML)[0]
            my_json = ",".join(my_json.split(',')[:-1])
            j = json.loads(my_json)
            room = j['room']

            fields = [
                'id', 'seq', 'building_floor', 'building_floor_str', 'room_floor', 'floor', 'deal_type', 'deposit',
                'price','elevator','heating','heating_type','jibun_address','road_address','detail_address',
                'maintenance','maintenance_cost','animal','parking','parking_cost','provision_size','room_size',
                'room_type','room_type_str','actived_time','selling_type','status'
            ]
            bang = dict()
            for f in fields:
                bang[f] = room[f]
            bang['location_lng'] = room['location'][0]
            bang['location_lat'] = room['location'][1]
            bang['option'] = ','.join(map(str, room['room_options']))

            bang['PartitionKey'] = str(bang['id'])
            bang['RowKey'] = str(bang['seq'])

            # pool = my_threading.MyThreadPool.instance()
            # pool.incr_count()
            store = storage.Storage()
            res = store.insert(bang)

        b.quit()
        print('[%s] %s' % ("duplicated" if res is None else "success", url))
        print('released bang: %s' % threading.activeCount())
