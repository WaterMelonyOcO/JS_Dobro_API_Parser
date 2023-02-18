import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import re
# какая-то хуита

# ссыка на дорых
URL_TEMPLATE = "https://dobro.ru/analytics"
r = requests.get(URL_TEMPLATE)
soup = bs(r.content, "html.parser")

# данные по россии
# получаю в массивы название и их значение в объект onMap


def getContent(linkType, linkCont):
    # Name = []
    # counts = []
    timeName = [types.text for types in soup.find_all(class_=linkType)]
    timeCount = [count.text for count in soup.find_all(class_=linkCont)]
    
    return [timeName, timeCount]


russMapData = getContent("js-map-analytics-type", "js-map-analytics-data")

# re.sub(r"<[^>]+>", "", str(tt.h3), flags=re.S)
# правая колонка
analit = [tt for tt in soup.find_all("div", class_="analytics")]
graphs = [tt.text for tt in analit[1].find_all("p")]
graphsName = ["ageCount","ageText", "womanProc", "womanText", "manProc", "manText"]
graphsCount = [graphs[0], graphs[1], graphs[2], graphs[3], graphs[4], graphs[5]]

# левая колонка
pTagL = analit[0].find_all("p")
hTagL = analit[0].find_all("h3")

leftColumtName = ["vacance", "vacCount","hours","hoursCount","", ""]
leftColumtCount = [pTagL[0].text, str(re.sub( r"<[^>]+>", "", str(hTagL[0]), flags=re.S)), pTagL[2].text, str(re.sub(r"<[^>]+>", "", str(hTagL[1]), flags=re.S)),"",""]



# преобразование в excel"graphRighStat": graphsName

df = pd.DataFrame({
    "voloters":russMapData[0],
    "volonterCount":russMapData[1],
    "graphRighStat": graphsName,
    "graphRighStatCount": graphsCount,
    "LeftColumtStat":leftColumtName,
    "LeftColumtStatCount":leftColumtCount
})

df.to_excel("./shit.xlsx")