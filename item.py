from bs4 import BeautifulSoup
import requests
# TODO maybe think about how many different websites this app will work on, and how they are going to be parsed. \
# TODO because some things need to be hardcoded


class AmazonItem:
    def __init__(self, url):
        self.url = url
        self.headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        self.amazon_soup = self.__get_soup()
        self.camel_soup = self.__get_camel_soup(self.__get_camel_url())
        self.title = self.__get_title()
        self.current_price = self.__get_price()
        self.highest_price = self.__get_highest_price()
        self.highest_price_date = self.__get_highest_price_date()
        self.lowest_price = self.__get_lowest_price()
        self.lowest_price_date = self.__get_lowest_price_date()
        self.avg_price = self.__get_avg_price()
        self.availability = self.__get_availability()

    def __get_soup(self):
        page = requests.get(self.url, headers=self.headers)
        soup1 = BeautifulSoup(page.content, 'html.parser')  # Need to do this twice for amazon.com
        soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')
        return soup2

    def __get_camel_url(self):  # TODO this function may be optimized with the .replace method
        url = self.url
        limit1 = 0
        limit2 = len(self.url)
        for x in range(22, len(url)):
            if x+1 < len(url):
                if(url[x]+url[x+1]) == 'dp':
                    limit1 = x
            if url[x] == '?':
                limit2 = x
                break
        return 'https://camelcamelcamel.com' + url[22:limit1] + 'product' + url[limit1+2:limit2]

    def __get_camel_soup(self, url):
        camel_page = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(camel_page.content, 'html.parser')
        return soup

    def __get_highest_price(self):
        price = self.camel_soup.find(class_='product_pane').find(class_='highest_price')
        if price is not None:
            return self.__str_to_float(price.contents[3].get_text())
        return -1

    def __get_highest_price_date(self):
        date = self.camel_soup.find(class_='product_pane').find(class_='highest_price')
        if date is not None:
            return date.contents[5].get_text()
        return "N/A"

    def __get_lowest_price(self):
        price = self.camel_soup.find(class_='product_pane').find(class_='lowest_price')
        if price is not None:
            return self.__str_to_float(price.contents[3].get_text())
        return -1

    def __get_lowest_price_date(self):
        price_date = self.camel_soup.find(class_="product_pane").find(class_='lowest_price')
        if price_date is not None:
            return price_date.contents[5].get_text()
        return "N/A"

    def __get_avg_price(self):
        price = self.camel_soup.find(class_="product_pane").contents[3]
        if len(price) > 3:
            price = price.contents[7].contents[3].get_text()
            return self.__str_to_float(price)
        return -1

    def __get_price(self):
        # Some items have special price boxes, so this should take care of that (this seems to happen)
        # when there is an item that is shipped outside of the US
        new_pitch_price = self.amazon_soup.find(id="newPitchPrice")
        if new_pitch_price is not None:
            dollars = new_pitch_price.find(class_="price-large").get_text().strip()
            cents = new_pitch_price.find(id="newPitchPrice")\
                          .find_all(class_="a-size-small price-info-superscript")[1].get_text().strip()
            return self.__str_to_float(dollars) + self.__str_to_float(cents)/100
        pos_promo_pitch_price = self.amazon_soup.find(id="posPromoPitchPrice")
        if pos_promo_pitch_price is not None:
            dollars = pos_promo_pitch_price.find(class_="a-section a-spacing-none").find(class_="price-large")\
                                        .get_text().strip()
            cents = pos_promo_pitch_price.find(class_="a-section a-spacing-none")\
                                        .find_all(class_="a-size-small price-info-superscript")[1].get_text().strip()

            return self.__str_to_float(dollars)+(self.__str_to_float(cents)/100)
        # if self.amazon.find(.contents/
        # price = self.amazon_soup.find(id="priceblock_ourprice").get_text()
        # return self.__str_to_float(price)
        return -1

    def __get_title(self):
        return self.amazon_soup.find(id="productTitle").get_text().strip()

    def __get_availability(self): # TODO implement this function correctly
        avail = self.amazon_soup.find(id="availabilityInsideBuyBox_feature_div")
        if avail is not None:
            avail = avail.find(id='availability')
            if avail is not None:
                return avail.get_text().strip()

        # print("current avail : ",x)
        return None

    def __str_to_float(self, s):  # This function will convert a string to a float
        s = s.replace('$', '')
        return float(s.replace(',', ''))

    def to_string(self):  # Just for debugging purposes.
        print(self.title)
        print("Current price = $", self.current_price)
        print("Highest price = $", self.highest_price, "\t", self.highest_price_date)
        print("Lowest price = $", self.lowest_price, "\t", self.lowest_price_date)
        print("Average price = $", self.avg_price)
        print("Current availability notes " , self.availability)
