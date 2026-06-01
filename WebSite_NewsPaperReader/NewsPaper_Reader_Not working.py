import requests
from bs4 import BeautifulSoup

url = "https://www.dailythanthi.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

text = soup.get_text(separator=" ")

print(text[:5000])