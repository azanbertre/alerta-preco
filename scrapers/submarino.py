from bs4 import BeautifulSoup

class Submarino:
    @classmethod
    def scrape(cls, html):
        soup = BeautifulSoup(html, 'html.parser')

        name = soup.find('h1', {'id': 'product-name-default'})
        price = soup.find('span', {'class': 'sales-price'})

        if name:
            name = name.getText().strip()

        if price:
            price = price.getText()
            if len(price.split(' ')) > 1:
                price = price.split(' ')[-1]
            price = float(price.replace('.', '').replace(',', '.'))

        return {'name': name, 'price': price}