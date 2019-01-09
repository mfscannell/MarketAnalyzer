import calendar
import datetime
import re
import time
import urllib
import urllib.request
import json
from py_finance import StockHistoryDict

class YahooFinanceClient:
    def __init__(self, tickerSymbol):
        self.tickerSymbol = tickerSymbol
    def printStock(self):
        print(self.tickerSymbol)
    def getHistory(self, fromDate, toDate):
        time_stamp_from = calendar.timegm(datetime.datetime.strptime(fromDate, "%Y-%m-%d").timetuple())
        time_stamp_to = calendar.timegm(datetime.datetime.strptime(toDate, "%Y-%m-%d").timetuple())
        quote_link = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history&crumb={}'

        attempts = 0
        while attempts < 5:
            crumble_str, cookie_str = self.__get_crumble_and_cookie(self.tickerSymbol)
            link = quote_link.format(self.tickerSymbol, time_stamp_from, time_stamp_to, crumble_str)
            request = urllib.request.Request(link, headers={'Cookie': cookie_str})

            try:
                response = urllib.request.urlopen(request)
                text = response.read()
                stockHitory = StockHistoryDict.toStockDict(text.decode("utf-8"))

                return stockHitory
            except urllib.error.URLError:
                attempts += 1
                time.sleep(2 * attempts)
        return []

    def __get_crumble_and_cookie(self, symbol):
        crumble_link = 'https://finance.yahoo.com/quote/{0}/history?p={0}'
        crumble_regex = r'CrumbStore":{"crumb":"(.*?)"}'
        cookie_regex = r'set-cookie: (.*?); '
        link = crumble_link.format(symbol)
        response = urllib.request.urlopen(link)
        match = re.search(cookie_regex, str(response.info()))
        cookie_str = match.group(1)
        text = response.read()
        match = re.search(crumble_regex, text.decode("utf-8"))
        crumble_str = match.group(1)
        return crumble_str, cookie_str