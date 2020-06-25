from enum import Enum
import requests
import random
import time
import json
import re

from urllib.parse import urlencode

from scrapers.casasbahia import CasasBahia
from scrapers.americanas import Americanas
from scrapers.submarino import Submarino
from scrapers.extra import Extra
from scrapers.magazineluiza import Magazine
from scrapers.amazon import Amazon

# for site to accept request
headers_list = [
    # Firefox 77 Mac
     {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Firefox 77 Windows
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Chrome 83 Mac
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    },
    # Chrome 83 Windows
    {
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }
]


class StoreEnum(Enum):
    CASASBAHIA = 0
    AMERICANAS = 1
    SUBMARINO = 2
    EXTRA = 3
    MAGAZINELUIZA = 4
    AMAZON = 5

    def to_name(self):
        if self == StoreEnum.CASASBAHIA:
            return 'casasbahia'
        elif self == StoreEnum.AMERICANAS:
            return 'americanas'
        elif self == StoreEnum.SUBMARINO:
            return 'submarino'
        elif self == StoreEnum.EXTRA:
            return 'extra'
        elif self == StoreEnum.MAGAZINELUIZA:
            return 'magazineluiza'
        elif self == StoreEnum.AMAZON:
            return 'amazon'

class App:
    def __init__(self, path):
        self.path = path
        self.post_url = None
        self.api_key = None
        self.products = []
        self.raw_products = []
        self.interval = 1

    def load_settings(self):
        with open(self.path, 'r') as f:
            data = json.load(f)
            self.raw_products = data.get('products', [])
            self.post_url = data.get('postUrl')
            self.api_key = data.get('apiKey')
            self.interval = int(data.get('interval', 1))
            if self.interval <= 0:
                self.interval = 1

    def load_products(self):
        self.products = []

        for product in self.raw_products:
            store = self.get_store(product['url'])

            self.products.append({
                'url': product['url'],
                'store': store,
                'html': self.get_content(product['url']),
                'supported': store != None,
                'price': product['price']
            })

    def get_store(self, url):
        host = self.get_host(url)
        if not host:
            return None

        for store in [{'name': s.to_name(), 'enum': s} for s in StoreEnum]:
            if store['name'] in host:
                return store['enum']

        return None

    def get_host(self, url):
        host = re.search(r"([a-z0-9\-\.]*)\.(([a-z]{2,4})|([0-9]{1,3}\.([0-9]{1,3})\.([0-9]{1,3})))", url)
        if host:
            host = str(host[0])
        return host

    def get_content(self, url):
        try:
            r = requests.get(url, headers=random.choice(headers_list))
        except Exception as e:
            print(e)
            return None

        return r.content

    def filter_prices(self, products):
        return [p for p in products if p['price'] and p['price'] < p['ideal_price']]

    def format_price(self, value):
        return "{:.2f}".format(value).replace('.', ',')

    def run(self):

        print("###Iniciando...")

        counter = 0
        while True:
            print("\n#Execução de index número {}".format(counter))

            self.load_products()

            results = []
            for product in self.products:
                if not product['supported']:
                    print('Loja {} não suportada'.format(
                        self.get_host(product['url'])
                    ))
                    continue
                if product['store'] == StoreEnum.CASASBAHIA:
                    result = CasasBahia.scrape(product['html'])
                elif product['store'] == StoreEnum.AMERICANAS:
                    result = Americanas.scrape(product['html'])
                elif product['store'] == StoreEnum.SUBMARINO:
                    result = Submarino.scrape(product['html'])
                elif product['store'] == StoreEnum.EXTRA:
                    result = Extra.scrape(product['html'])
                elif product['store'] == StoreEnum.MAGAZINELUIZA:
                    result = Magazine.scrape(product['html'])
                elif product['store'] == StoreEnum.AMAZON:
                    result = Amazon.scrape(product['html'])

                result['store'] = product['store'].to_name()
                result['ideal_price'] = product['price']
                results.append(result)

            print(" - Encontrado {} produto(s)".format(len(results)))

            if not self.api_key and self.post_url:
                requests.post(self.post_url, json={'results': results})

                print("#Dormindo por {} minuto(s)".format(self.interval))
                time.sleep(self.interval * 60)
                continue

            if self.api_key:
                results = self.filter_prices(results)

                print(" - {} produto(s) com preço abaixo do desejado".format(len(results)))

                if not results:
                    print("#Dormindo por {} minuto(s)".format(self.interval))
                    time.sleep(self.interval * 60)
                    continue

                join_push_url = "https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?deviceId=group.all"

                text=""
                for result in results:
                    text += "\n{} está por R$ {} na loja {}. Preço desejado: R$ {}\n".format(
                        result['name'],
                        self.format_price(result['price']),
                        result['store'],
                        self.format_price(result['ideal_price'])
                    )

                join_push_url += "&{}&{}&apikey={}".format(
                    urlencode({"text": text}),
                    urlencode({"title": "{} produto(s) estão abaixo do preço desejado!!!".format(len(results))}), self.api_key)

                requests.post(join_push_url)

            print("#Dormindo por {} minuto(s)".format(self.interval))
            time.sleep(self.interval * 60)
