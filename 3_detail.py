import requests
from bs4 import BeautifulSoup

url_movie = 'https://www.dytt8.net//html/gndy/dyzz/20201220/60866.html'

response = requests.get(url_movie).content

soup = BeautifulSoup(response, 'html.parser')

div_content = soup.find('div', {'class': 'co_content8'})

content = div_content.get_text().strip()

content = str(content).replace('◎', '')

print(content)

with open('1.txt', 'wb') as f:
    f.write(content)


