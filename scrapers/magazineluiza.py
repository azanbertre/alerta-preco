from bs4 import BeautifulSoup

class Magazine:
    @classmethod
    def scrape(cls, html):
        soup = BeautifulSoup(html, 'html.parser')

        name = soup.find('h1', {'class': 'header-product__title'}).getText()
        price = soup.find('span', {'class': 'price-template__text'}).getText()

        if price:
            price = float(price.replace('.', '').replace(',', '.'))

        return {'name': name, 'price': price}