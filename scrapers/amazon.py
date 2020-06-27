from bs4 import BeautifulSoup

class Amazon:
    @classmethod
    def scrape(cls, html):
        soup = BeautifulSoup(html, 'html.parser')

        name = soup.find('span', {'id': 'productTitle'})
        price = soup.find('span', {'id': 'priceblock_ourprice'})

        if name:
            name = name.getText().strip()
        if price:
            price = price.getText().split('$')[-1]
            price = float(price.replace('.', '').replace(',', '.'))

        return {'name': name, 'price': price}