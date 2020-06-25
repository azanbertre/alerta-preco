from bs4 import BeautifulSoup

class Extra:
    @classmethod
    def scrape(cls, html):
        soup = BeautifulSoup(html, 'html.parser')

        name = soup.find('h1', {'class': 'fn name'}).getText()
        price = soup.find('i', {'class': 'sale price'}).getText()

        if price:
            price = float(price.replace('.', '').replace(',', '.'))

        return {'name': name, 'price': price}