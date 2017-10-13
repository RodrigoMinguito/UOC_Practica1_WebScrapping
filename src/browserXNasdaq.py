from browserBase import BrowserBase
from bs4 import BeautifulSoup

class BrowserXYahoo(BrowserBase):
    def __init__(self):
        self.browser_id = "NASDAQ"
        self.browser_web = "http://www.nasdaq.com/es/symbol/"

    def getData(self):
        soup = BeautifulSoup(self.pagina.content, 'html.parser')
        self.currentVolume = self.getCurrentVolume(soup)
        self.usualVolume = self.getUsualVolume(soup)
        self.currentTime = self.getCurrentTime(soup)

    def getCurrentVolume(self, soup):
        ret = "NA"
        try:
            ret = soup.find('label', attrs={'id': self.tickler+'_Volume'}).string
        except:
            ret = "NA"
        return ret

    def getUsualVolume(self,soup):
        ret = "NA"
        vol = soup.find('table', attrs={'id': 'quotes_content_left_InfoQuotesResults'})
        j=0
        for child in vol.descendants:
            j=j+1
            try:
                if j==70:
                    return child
            except:
                ret = "NA"
        return ret

    def getCurrentTime(self,soup):
        ret = "NA"
        try:
            vol = soup.find('span', attrs={'id': 'qwidget_markettime'})
            ret=vol.string
        except:
            ret="NA"
        return ret

def create():
    myInstance = BrowserXNasdaq()
    return myInstance