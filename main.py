import requests
from bs4 import BeautifulSoup
import re
from dataclasses import dataclass


@dataclass
class ShopItem:
    znamka: str
    vrsta: str
    kolicina: str
    cena: str


def getItemText(items):
    content = []
    for item in items:
        pattern = r"<.*?>"
        res = re.sub(pattern, "", item)
        #res = res.replace("\n", "")
        content.append(res)
    return content


def parseStringToDataclass(string):
    splits = string.split('\n')
    item = ShopItem("", "", "", "")
    item.znamka = splits[0]
    ss = splits[1].split(",", 1)
    item.vrsta = ss[0]
    item.kolicina = ss[1]
    found = False
    for s in splits:
        if '€' in s and not found:
            item.cena = s
            found = True
    return item


url = "https://www.hofer.si/sl/sortiment/novo.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
items = soup.find_all("div", "item")
count = 0

for item in items:
    ps = item.find_all("p")
    resultStrings = [str(p) for p in ps]
    res = getItemText(resultStrings)
    for r in res:
        shopitem = parseStringToDataclass(r)
        print(shopitem)