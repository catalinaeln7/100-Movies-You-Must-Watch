import requests
from bs4 import BeautifulSoup

response = requests.get(url="https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features"
                            "/best-movies-2/")
response.raise_for_status()
empire_website = response.text

soup = BeautifulSoup(empire_website, "html.parser")
print(soup.prettify())
