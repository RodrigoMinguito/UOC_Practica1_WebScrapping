import os
from time import gmtime, strftime
import requests
from bs4 import BeautifulSoup
from browserBase import BrowserBase

def findHandlers():
    subclasses = []

    def look_for_subclass(modulename):
        module = __import__(modulename)

        # walk the dictionaries to get to the last one
        d = module.__dict__
        for m in modulename.split('.')[1:]:
            d = d[m].__dict__

        # look through the dictionary
        for key, value in d.items():
            if key == BrowserBase.__name__:
                continue

            try:
                if issubclass(value, BrowserBase):
                    subclasses.append(module.create())
            except TypeError:
                continue

    for root, dirs, files in os.walk(os.getcwd()):
        for name in files:
            if name.endswith(".py") and name.startswith("browserX"):
                modulename = name.rsplit('.', 1)[0]
                print(modulename)
                look_for_subclass(modulename)

    return subclasses


#Get scripts to get data	
theCollectorHandlers = findHandlers()


#get Ticklers to collect
listTicklers = []
nasdaq_list_origin = 'https://es.wikipedia.org/wiki/NASDAQ-100'
page = requests.get(nasdaq_list_origin)
soup = BeautifulSoup(page.content, 'html.parser')
lista = soup.find_all('li', attrs={'class': '', 'id': ''})

for elem in lista:
    for key in elem.contents:
        try:
            newKey = key.strip()
            if (newKey.find("(") > -1 and newKey.find(")") > -1):
                tickler = newKey[newKey.find("(") + 1:newKey.find(")")]
                if tickler not in listTicklers:
                    listTicklers.append(tickler)
        except:
            continue

listTicklers.sort()

with open('index2.csv', 'a') as fileCSV:
    for tickler in listTicklers:
        print("\n" + tickler)
        listaResults = []
        for handler in theCollectorHandlers:
            handler.getInfo(tickler, listaResults)
        generatedData = tickler + ";" + strftime("%d/%m/%Y %H:%M:%S", gmtime())
        for res in listaResults:
            generatedData = generatedData + ";" + res
        fileCSV.write(generatedData + "\n")
        print(generatedData)
fileCSV.close()
