import re
from datetime import datetime
import requests

class BrowserBase(object):
    browser_id = "base"
    browser_web = "none"
    currentVolume = "NA"
    usualVolume = "NA"
    currentTime = "NA"
    tickler = ""
    page = ""
    pagina = ""

    def __init__(self):
        pass

    def getData(self, tickler):
        raise NotImplementedError

    def getInfo(self, tickler, listaResultado):
        try:
            self.tickler = tickler
            self.page = self.browser_web + self.tickler
            self.pagina = requests.get(self.page)
            self.getData()
            self.currentVolume = self.cleanNumericString(self.currentVolume)
            self.usualVolume = self.cleanNumericString(self.usualVolume)
            self.currentTime = self.cleanTime(self.currentTime)
            listaResultado.append(
                self.currentTime + ";" + self.currentVolume + ";" + self.usualVolume)
        except Exception as inst:
            print(inst)
            listaResultado.append("NA;NA;NA")

    def cleanNumericString(self, strg):
        s = strg.replace(",", "").replace(".00", "")
        if re.match(".*\...M", s):
            s = s + "0000"
        if re.match(".*\..M", s):
            s = s + "00000"
        if re.match(".*\.M", s):
            s = s + "000000"
        if (re.match(".*M", s) and not (re.match(".*\.M", s) or re.match(".*\..M", s) or re.match(".*\...M", s))):
            s = s + "0000000"
        s = s.replace(".", "").replace("M", "")
        if s.isnumeric():
            return s
        return "NA"

    def cleanTime(self, strgIN):
        if 'As of ' in strgIN:
            strgIN = strgIN.replace('As of ', '').replace('. Market open.', '')
        if 'Real-time:' in strgIN:
            strgIN = strgIN.replace("NASDAQ", "      NASDAQ")
            posIni = strgIN.find('Real-time:') + 10
            strgIN = strgIN[posIni:posIni + 14]
        if ', ' in strgIN:
            strg2 = strgIN.split(',')[1].split(' ')
            strgIN = strg2[2]
        strgIN = strgIN.replace(" EDT", "")
        strgIN = strgIN.replace(" EDT", "")
        strgIN = strgIN.strip()
        if len(strgIN) > 10:
            return "NA"
        if ("PM" in strgIN or 'AM' in strgIN):
            strgIN = strgIN.replace(" AM", "AM")
            strgIN = strgIN.replace(" PM", "PM")
            in_time = datetime.strptime(strgIN, "%I:%M%p")
            out_time = datetime.strftime(in_time, "%H:%M")
            strgIN = out_time
        return strgIN.strip()

    def getCurrentVolume(self):
        raise NotImplemented

    def getUsualVolume(self):
        raise NotImplemented

    def getCurrentTime(self):
        raise NotImplemented

def create():
    myInstance = BrowserBase()
    return myInstance
