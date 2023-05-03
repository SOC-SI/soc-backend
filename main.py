import requests
from bs4 import BeautifulSoup
import re


def getItemText(item):
    pattern = r"<.*?>"
    content = re.sub(pattern, "", item)
    return content


url = "https://www.hofer.si/sl/sortiment/novo.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
items = soup.find_all("div", "item")
for item in items:
    ps = item.find_all("p")
    resultStrings = [str(p) for p in ps]
    for string in resultStrings:
        rx = getItemText(string)
        print(rx)
