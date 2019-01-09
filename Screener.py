from py_finance import YahooFinanceClient
import csv
from statistics import mean

buySignal = 20
sellSignal = 80
obvSignal = 10
lastStochasticNumPeriods = 39
obvBestFitNumPeriods = 5

def findLowestLow(tradingDaysList, start, stop, attribute = ''):
    lowestLow = 0
    
    if attribute == '':
        lowestLow = tradingDaysList[start]
    else:
        lowestLow = tradingDaysList[start][attribute]
    
    for i in range(start, stop + 1):
        if attribute == '':
            if tradingDaysList[i] < lowestLow:
                lowestLow = tradingDaysList[i]
        else:
            if tradingDaysList[i][attribute] < lowestLow:
                lowestLow = tradingDaysList[i][attribute]
            
    return lowestLow
    
def findHighestHigh(tradingDaysList, start, stop, attribute = ''):
    highestHigh = 0
    
    if attribute == '':
        highestHigh = tradingDaysList[start]
    else:
        highestHigh = tradingDaysList[start][attribute]
    
    for i in range(start, stop + 1):
        if attribute == '':
            if tradingDaysList[i] > highestHigh:
                highestHigh = tradingDaysList[i]
        else:
            if tradingDaysList[i][attribute] > highestHigh:
                highestHigh = tradingDaysList[i][attribute]
            
    return highestHigh
    
# Find the simple average of all items in the list from index start to index stop inclusive
def findSimpleAverage(aList, start, stop, attribute = ''):
    sum = 0
    
    for i in range(start, stop + 1):
        if attribute == '':
            sum = sum + aList[i]
        else:
            sum = sum + aList[i][attribute]
        
    return sum / (stop - start + 1)
    
# Find numerator
def findNumerator(xList, xAvg):
    sum = 0

# Find the denominator for Best fit slope calc
def findDenominator(aList, start, stop, avgValue, attribute = ''):
    sum = 0
    
    for i in range(start, stop + 1):
        if attribute == '':
            sum = sum + (aList[i] - avgValue) ** 2
        else:
            sum = sum + (aList[i][attribute] - avgValue) ** 2
            
    return sum
    
    
def findBestFitSlope(aList, start, stop, xAttribute, yAttribute):
    bestFitSlope = 0
    
    averageX = findSimpleAverage(tradingDays, start, stop, xAttribute)
    averageY = findSimpleAverage(tradingDays, start, stop, yAttribute)
    denominator = 0
    numerator = 0
    
    for i in range(start, stop + 1):
        denominator = denominator + (tradingDays[i][xAttribute] - averageX) ** 2
        
    for i in range(start, stop + 1):
        numerator = numerator + (tradingDays[i][xAttribute] - averageX) * (tradingDays[i][yAttribute] - averageY)
    
    return numerator / denominator
    
    
# Start of program
print("S & P 500: ^GSPC")
print("Nasdaq: ^IXIC")
print("Russell 2000: ^RUT")
stockSymbol = input("Enter stock symbol:")
startDate = input("Start date (yyyy-mm-dd):")
endDate = input("End date (yyyy-mm-dd):")

stockClient = YahooFinanceClient.YahooFinanceClient(stockSymbol)
tradingDays = stockClient.getHistory(startDate, endDate)



for i, tradingDay in enumerate(tradingDays):
    # calc OBV
    if i == 0:
        tradingDays[i]['OBV'] = tradingDays[i]['Volume']
    elif tradingDays[i]['Close'] > tradingDays[i - 1]['Close']:
        tradingDays[i]['OBV'] = tradingDays[i - 1]['OBV'] + tradingDays[i]['Volume']
    elif tradingDays[i]['Close'] < tradingDays[i - 1]['Close']:
        tradingDays[i]['OBV'] = tradingDays[i - 1]['OBV'] - tradingDays[i]['Volume']
    elif tradingDays[i]['Close'] == tradingDays[i - 1]['Close']:
        tradingDays[i]['OBV'] = tradingDays[i - 1]['OBV']
        
    # calc OBV best fit slope
    if i >= obvBestFitNumPeriods:
        obvBestFitSlope = findBestFitSlope(tradingDays, i - (obvBestFitNumPeriods - 1), i, 'Period', 'OBV')
        tradingDays[i]['OBVSlope'] = obvBestFitSlope
    else:
        tradingDays[i]['OBVSlope'] = 0
    
    
    # calc OBV avgs
    if i >= obvSignal:
        tradingDays[i]['OBV' + str(obvSignal) + 'Avg'] = findSimpleAverage(tradingDays, i - (obvSignal - 1), i, 'OBV')
    else:
        tradingDays[i]['OBV' + str(obvSignal) + 'Avg'] = 0

    # calc last stochastic
    if i >= lastStochasticNumPeriods:
        lowestLow39 = findLowestLow(tradingDays, i - (lastStochasticNumPeriods - 1), i, 'Low')
        highestHigh39 = findHighestHigh(tradingDays, i - (lastStochasticNumPeriods - 1), i, 'High')
        tradingDays[i]['LastStochastic'] = 100 * (tradingDays[i]['Close'] - lowestLow39) / (highestHigh39 - lowestLow39)
    else:
        tradingDays[i]['LastStochastic'] = 0


#determine buy and sell signals
for m, tradingDay in enumerate(tradingDays):
    buySell = 'HOLD'
    
    if (m > 0 and 
        tradingDays[m]['LastStochastic'] > tradingDays[m - 1]['LastStochastic'] and 
        tradingDays[m]['OBVSlope'] > 0
        #tradingDay['LastStochastic'] > buySignal and 
        #tradingDays[m - 1]['LastStochastic'] < buySignal and 
        #tradingDay['OBV'] > tradingDay['OBV' + str(obvSignal) + 'Avg']
       ):
        buySell = 'BUY'
        
    if (m > 0 and 
        tradingDays[m]['LastStochastic'] < tradingDays[m - 1]['LastStochastic'] and 
        tradingDays[m]['OBVSlope'] < 0
        #tradingDay['LastStochastic'] < sellSignal and 
        #tradingDay['OBV'] < tradingDay['OBV' + str(obvSignal) + 'Avg']
       ):
        buySell = 'SELL'
        
    tradingDays[m]['Buy/Sell'] = buySell
        
    print('Period:' + str(tradingDay['Period']) + ', Date:' + tradingDay['Date'] + ', Last:' + str(round(tradingDay['Close'], 2)) + ', Vol:' + str(tradingDay['Volume']) + ', LastSto:' + str(round(tradingDay['LastStochastic'], 1)) + ', OBV:' + str(tradingDay['OBV']) + ', OBVAvg:' + str(tradingDay['OBV' + str(obvSignal) + 'Avg']) + ', OBVSlope:' + str(tradingDay['OBVSlope']) + ', B/S:' + buySell)

'''
keys = tradingDays[0].keys()
with open('C:/temp/flashBackup/_stocks/historicalSPLast2007_2019BestFit.csv', 'w', newline = '') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(tradingDays)
'''

