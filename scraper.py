# pip install request bs4
import requests
from bs4 import BeautifulSoup
import smtplib  # This is just a protocol that sends emails
from item import AmazonItem  # Items object which will contain its information (price)

URL = 'https://www.amazon.com/BIC-Round-Ballpoint-Medium-60-Count/dp/B0012YVGOW?ref_=Oct_' \
      'DLandingS_PC_6a44c109_0&smid=ATVPDKIKX0DER&th=1&psc=1'

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

page = requests.get(URL, headers=headers)

def check_price():
    # because amazon.com is written in javascript, I need to do this twice so I can access the elements I need
    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

    title = soup2.find(id="productTitle").get_text()
    price = soup2.find(id="priceblock_ourprice").get_text()

    converted_price = float(price[1:])
    ideal_amount = 4.99
    print(title.strip())
    print(converted_price)

    # if converted_price ideal_amount:
    #     send_mail()


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo() # TODO read about ehlo()
    server.starttls()
    server.ehlo()

    server.login('sebascaicedo25@gmail.com', 'vhhrbzhfcvoyffkz')

    subject = 'Price fell down'
    body = 'Check the amazon link: https://www.amazon.com/BIC-Round-Ballpoint-Medium-60-Count/dp/B0012YVGOW?ref_=Oct_' \
           'DLandingS_PC_6a44c109_0&smid=ATVPDKIKX0DER&th=1&psc=1'

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'sebascaicedo25@gmail.com',
        'sebascaicedo-01@hotmail.com',
        msg
    )
    print("EMAIL HAS BEEN SENT!")

    server.quit()


# check_price()
temp = AmazonItem(URL)
# test = temp.camel_soup
# print(type(test.find(id='histories')))
# x = test.find(class_='lowest_price').contents[5].contents[0]
# x = temp.amazon_soup.find(id="productTitle")
x = temp.title
print(x)
# print(temp.strip_str_to_float(x))



