from bs4 import BeautifulSoup

class CasasBahia:
    @classmethod
    def scrape(cls, html):
        soup = BeautifulSoup(html, 'html.parser')

        name = soup.find('h1', {'class': 'fn name'})
        price = soup.find('i', {'class': 'sale price'})

        if name:
            name = name.getText().strip()

        if price:
            price = float(price.getText().replace('.', '').replace(',', '.'))

        return {'name': name, 'price': price}