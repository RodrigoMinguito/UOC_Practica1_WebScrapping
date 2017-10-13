from browserBase import BrowserBase
from bs4 import BeautifulSoup

class BrowserXYahoo(BrowserBase):
    def __init__(self):
        self.browser_id = "YAHOO"
        self.browser_web = "https://finance.yahoo.com/quote/"

    def getData(self):
        soup = BeautifulSoup(self.pagina.content, 'html.parser')
        self.currentVolume = self.getCurrentVolume(soup)
        self.usualVolume = self.getUsualVolume(soup)
        self.currentTime = self.getCurrentTime(soup)

    def getCurrentVolume(self, soup):
        ret = "NA"
        vol = soup.find('td', attrs={'data-test': 'TD_VOLUME-value'})
        for child in vol.descendants:
            try:
                for child2 in child.strings:
                    return child2
            except:
                ret="NA"
        return ret

    def getUsualVolume(self,soup):
        ret = "NA"
        vol = soup.find('td', attrs={'data-test': 'AVERAGE_VOLUME_3MONTH-value'})
        for child in vol.descendants:
            try:
                for child2 in child.strings:
                    return child2
            except:
                ret = "NA"
        return ret

    def getCurrentTime(self,soup):
        ret = "NA"
        try:
            vol = soup.find('div', attrs={'id': 'quote-market-notice'})
            ret=vol.string
        except:
            ret="NA"
        return ret

def create():
    myInstance = BrowserXYahoo()
    return myInstance