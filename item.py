from bs4 import BeautifulSoup
import requests
# TODO maybe think about how many different websites this app will work on, and how they are going to be parsed. \
# TODO because some things need to be hardcoded
class AmazonItem:
    def __init__(self, URL):
        self.URL = URL
        self.headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        self.soup = self.get_soup()

    def get_soup(self):
        page = requests.get(self.URL, headers=self.headers)
        soup1 = BeautifulSoup(page.content, 'html.parser')  # Need to do this twice for amazon.com
        soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')
        return soup2

    def get_camel_url(self):
        url = self.get_url()
        limit1 = 0;
        limit2 = 0;
        for x in range(22, len(url)):
            if(url[x]+url[x+1]) == 'dp':
                limit1 = x
            if url[x] == '?':
                limit2 = x
                break
        return 'https://camelcamelcamel.com' + url[22:limit1] + 'product' + url[limit1+2:limit2]

    def get_price(self):
        return float(self.soup.find(id="priceblock_ourprice").get_text()[1:])

    # def getTitle(self):

    def get_url(self):
        return self.URL


# p1 = Item(4)
# p1.getx()
