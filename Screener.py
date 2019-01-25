from py_finance import YahooFinanceClient
from py_finance import TechnicalAnalysis
import Statistics
import csv
from statistics import mean

buySignal = 20
sellSignal = 80

obvSMANumPeriods = 5
obvBestFitNumPeriods = 5

adBestFitNumPeriods = 5

slowStochasticNumPeriods = 39
slowStochasticBestFitNumPeriods = 5
    
# Start of program
print("S & P 500: ^GSPC")
print("NYSE: ^NYA")
print("Nasdaq: ^IXIC")
print("Russell 2000: ^RUT")
print("VIX: ^VIX")
stockSymbol = input("Enter stock symbol:")
startDate = input("Start date (yyyy-mm-dd):")
endDate = input("End date (yyyy-mm-dd):")

stockClient = YahooFinanceClient.YahooFinanceClient(stockSymbol)
tradingDays = stockClient.getHistory(startDate, endDate)

vixTradingDays = []

vixStockClient = YahooFinanceClient.YahooFinanceClient("^VIX")

if stockSymbol != "^VIX":
    vixTradingDays = vixStockClient.getHistory(startDate, endDate)

for i, tradingDay in enumerate(tradingDays):
    tradingDays[i]['OBV'] = TechnicalAnalysis.calcOBV(tradingDays, i)
        
    # calc OBV best fit slope
    if i >= obvBestFitNumPeriods:
        tradingDays[i]['OBVSlope'] = Statistics.findBestFitSlope(tradingDays, i - (obvBestFitNumPeriods - 1), i, 'Period', 'OBV')
    else:
        tradingDays[i]['OBVSlope'] = 0

    tradingDays[i]['AD'] = TechnicalAnalysis.calcAccumDist(tradingDays, i)

    # calc A/D best fit
    if i >= adBestFitNumPeriods:
        tradingDays[i]['ADSlope'] = Statistics.findBestFitSlope(tradingDays, i - (adBestFitNumPeriods - 1), i, 'Period', 'AD')
    else:
        tradingDays[i]['ADSlope'] = 0

    # calc slow stochastic
    if i >= slowStochasticNumPeriods:
        tradingDays[i]['SlowStochastic'] = TechnicalAnalysis.calcSlowStochastic(tradingDays, i - (slowStochasticNumPeriods - 1), i)
    else:
        tradingDays[i]['SlowStochastic'] = 0
        
    # calc slow stochastic 1 day slope
    if i >= 1:
        tradingDays[i]['SlowSto1DaySlope'] = tradingDays[i]['SlowStochastic'] - tradingDays[i - 1]['SlowStochastic']
    else:
        tradingDays[i]['SlowSto1DaySlope'] = 0
        
    # calc slow stochastic best fit
    if i >= slowStochasticBestFitNumPeriods:
        tradingDays[i]['SlowStoSlope'] = Statistics.findBestFitSlope(
        tradingDays, i - (slowStochasticBestFitNumPeriods - 1), i, 'Period', 'SlowStochastic')
    else:
        tradingDays[i]['SlowStoSlope'] = 0

    #VIX stuff
    if stockSymbol != "^VIX":
        tradingDays[i]["VIXOpen"] = vixTradingDays[i]["Open"]
        tradingDays[i]["VIXHigh"] = vixTradingDays[i]["High"]
        tradingDays[i]["VIXLow"] = vixTradingDays[i]["Low"]
        tradingDays[i]["VIXClose"] = vixTradingDays[i]["Close"]
        
        # calc slow stochastic
        if i >= slowStochasticNumPeriods:
            tradingDays[i]['VIXSlowStochastic'] = TechnicalAnalysis.calcSlowStochastic(vixTradingDays, i - (slowStochasticNumPeriods - 1), i)
        else:
            tradingDays[i]['VIXSlowStochastic'] = 0
            
        # calc slow stochastic 1 day slope
        if i >= 1:
            tradingDays[i]['VIXSlowSto1DaySlope'] = tradingDays[i]['VIXSlowStochastic'] - tradingDays[i - 1]['VIXSlowStochastic']
        else:
            tradingDays[i]['VIXSlowSto1DaySlope'] = 0


#determine buy and sell signals
for m, tradingDay in enumerate(tradingDays):
    buySell = 'HOLD'
    
    if (m > 0 and 
        tradingDays[m]['SlowStochastic'] > tradingDays[m - 1]['SlowStochastic'] and 
        tradingDays[m]['ADSlope'] > 0
       ):
        buySell = 'BUY'
        
    if (m > 0 and 
        tradingDays[m]['SlowStochastic'] < tradingDays[m - 1]['SlowStochastic'] and 
        (tradingDays[m]['ADSlope'] < 0 or tradingDays[m]['OBVSlope'] < 0)
       ):
        buySell = 'SELL'
        
    tradingDays[m]['Buy/Sell'] = buySell

    print('Period:' + str(tradingDay['Period']) + ', Date:' + tradingDay['Date'] + ', Last:' + str(round(tradingDay['Close'], 2)) + ', Vol:' + str(tradingDay['Volume']) + ', SlowSto:' + str(round(tradingDay['SlowStochastic'], 1)) + ', OBVSlope:' + str(round(tradingDay['OBVSlope'], 1)) + ', ADSlope:' + str(round(tradingDay['ADSlope'], 1)) + ', B/S:' + buySell)

'''
keys = tradingDays[0].keys()
with open('C:/temp/flashBackup/_stocks/WithVix.csv', 'w', newline = '') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(tradingDays)
'''

