from bs4 import BeautifulSoup

class Magazine:
    @classmethod
    def scrape(cls, html):
        soup = BeautifulSoup(html, 'html.parser')

        name = soup.find('h1', {'class': 'header-product__title'})
        price = soup.find('span', {'class': 'price-template__text'})

        if name:
            name = name.getText().strip()

        if price:
            price = float(price.getText().replace('.', '').replace(',', '.'))

        return {'name': name, 'price': price}