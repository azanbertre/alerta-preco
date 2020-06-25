from bs4 import BeautifulSoup

class Amazon:
    @classmethod
    def scrape(cls, html):
        soup = BeautifulSoup(html, 'html.parser')

        name = soup.find('span', {'id': 'productTitle'}).getText().strip()
        price = soup.find('span', {'id': 'priceblock_ourprice'}).getText()

        if price:
            price = price.split('$')[-1]
            price = float(price.replace('.', '').replace(',', '.'))

        return {'name': name, 'price': price}