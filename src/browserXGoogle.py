from browserBase import BrowserBase
from bs4 import BeautifulSoup

class BrowserXYahoo(BrowserBase):
    def __init__(self):
        self.browser_id = "GOOGLE"
        self.browser_web = "https://finance.google.com/finance?q="

    def getData(self):
        soup = BeautifulSoup(self.pagina.content, 'html.parser')
        self.currentVolume = self.getCurrentVolume(soup)
        self.usualVolume = self.getUsualVolume(soup)
        self.currentTime = self.getCurrentTime(soup)

    def getCurrentVolume(self, soup):
        ret = "NA"
        vol = soup.find_all('td', attrs={'class': 'val'})
        try:
            i = 0
            for child in vol:
                i = i + 1
                if (i == 4):
                    return child.string.split("/")[0]
        except:
            ret = "NA"
        return ret

    def getUsualVolume(self, soup):
        vol = soup.find_all('td', attrs={'class': 'val'})
        ret = "NA"
        try:
            i = 0
            for child in vol:
                i = i + 1
                if (i == 4):
                    return child.string.split("/")[1].replace('\n', '').replace('\r', '')
        except:
            ret = "NA"
        return ret

    def getCurrentTime(self, soup):
        ret = "NA"
        rets = soup.find_all('div')
        i = 0
        for k in rets:
            i = i + 1
            try:
                if i == 38:
                    return k.text.replace("\n", "").replace("\r", "")
            except:
                ret = "NA"
        return ret

def create():
    myInstance = BrowserXGoogle()
    return myInstance
