import requests
from bs4 import BeautifulSoup
import codecs

url_movie = 'https://www.dytt8.net//html/gndy/dyzz/20201220/60866.html'

response = requests.get(url_movie).content

soup = BeautifulSoup(response, 'html.parser')

div_content = soup.find('div', {'class': 'co_content8'})

content = div_content.get_text().strip()


# todo: this is important
# content = content.encode('cp1252', 'ignore').decode('gb2312', 'ignore')


# content = content.encode('ISO-8859-1', 'ignore').decode('gb2312', 'ignore')
content = content.encode('latin-1', 'ignore').decode('gb2312', 'ignore')



print(content)

# a = codecs.encode(content)
# print(a)

# print(content)

with open('1.txt', 'w') as f:
    f.write(content)


