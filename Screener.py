from py_finance import YahooFinanceClient
from py_finance import TechnicalAnalysis
import Statistics
import csv
from statistics import mean

obvBestFitNumPeriods = 5

adBestFitNumPeriods = 5

bestFitNumPeriods = [3, 4, 5]

slowStochasticNumPeriods = 39
slowStochasticBestFitNumPeriods = 3

rsiNumPeriods = 14
    
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

print('Calculating technical analysis...')
for i, tradingDay in enumerate(tradingDays):
    tradingDays[i]['OBV'] = TechnicalAnalysis.calcOBV(tradingDays, i)
        
    # calc OBV best fit slopes
    for numPeriods in bestFitNumPeriods:
        if i >= numPeriods:
            tradingDays[i]['OBV' + str(numPeriods) + 'DaySlope'] = Statistics.findBestFitSlope(tradingDays, i - (numPeriods - 1), i, 'Period', 'OBV')
        else:
            tradingDays[i]['OBV' + str(numPeriods) + 'DaySlope'] = 0

    tradingDays[i]['AD'] = TechnicalAnalysis.calcAccumDist(tradingDays, i)

    # calc A/D best fit
    for numPeriods in bestFitNumPeriods:
        if i >= numPeriods:
            tradingDays[i]['AD' + str(numPeriods) + 'DaySlope'] = Statistics.findBestFitSlope(tradingDays, i - (numPeriods - 1), i, 'Period', 'AD')
        else:
            tradingDays[i]['AD' + str(numPeriods) + 'DaySlope'] = 0

    # calc slow stochastic
    if i >= slowStochasticNumPeriods:
        tradingDays[i]['SlowStochastic'] = TechnicalAnalysis.calcSlowStochastic(tradingDays, i - (slowStochasticNumPeriods - 1), i)
    else:
        tradingDays[i]['SlowStochastic'] = 0
        
    # calc slow stochastic 1 day slope
    if i >= 1:
        tradingDays[i]['SlowSto1DaySlope'] = tradingDays[i]['SlowStochastic'] - tradingDays[i - 1]['SlowStochastic']
        
        if tradingDays[i - 1]['SlowStochastic'] > 0:
            tradingDays[i]['SlowSto1DayPercentSlope'] = 100 * tradingDays[i]['SlowSto1DaySlope'] / tradingDays[i - 1]['SlowStochastic']
        else:
            tradingDays[i]['SlowSto1DayPercentSlope'] = 1000
    else:
        tradingDays[i]['SlowSto1DaySlope'] = 0
        tradingDays[i]['SlowSto1DayPercentSlope'] = 0
        
    # calc Slow Stochastic best fit slopes
    for numPeriods in bestFitNumPeriods:
        if i >= numPeriods:
            tradingDays[i]['SlowSto' + str(numPeriods) + 'DaySlope'] = Statistics.findBestFitSlope(tradingDays, i - (numPeriods - 1), i, 'Period', 'SlowStochastic')
        else:
            tradingDays[i]['SlowSto' + str(numPeriods) + 'DaySlope'] = 0
            
    TechnicalAnalysis.calcRsi(tradingDays, i, rsiNumPeriods)
    
    # calc RSI 1 day slope
    if i >= 1:
        tradingDays[i]['14DayRSI1DaySlope'] = tradingDays[i]['14DayRSI'] - tradingDays[i - 1]['14DayRSI']
    else:
        tradingDays[i]['14DayRSI1DaySlope'] = 0
        
    # calc RSI best fit slopes
    for numPeriods in bestFitNumPeriods:
        if i >= numPeriods:
            tradingDays[i]['14DayRSI' + str(numPeriods) + 'DaySlope'] = Statistics.findBestFitSlope(tradingDays, i - (numPeriods - 1), i, 'Period', '14DayRSI')
        else:
            tradingDays[i]['14DayRSI' + str(numPeriods) + 'DaySlope'] = 0

    #VIX stuff
    if stockSymbol != "^VIX":
        tradingDays[i]["VIXOpen"] = vixTradingDays[i]["Open"]
        tradingDays[i]["VIXHigh"] = vixTradingDays[i]["High"]
        tradingDays[i]["VIXLow"] = vixTradingDays[i]["Low"]
        tradingDays[i]["VIXClose"] = vixTradingDays[i]["Close"]
        
        # calc VIX slope
        if i >= 1:
            tradingDays[i]['VIX1DaySlope'] = tradingDays[i]['VIXClose'] - tradingDays[i - 1]['VIXClose']
            tradingDays[i]['VIX1DayPercentSlope'] = 100 * tradingDays[i]['VIX1DaySlope'] / tradingDays[i - 1]['VIXClose']
        else:
            tradingDays[i]['VIX1DaySlope'] = 0
            tradingDays[i]['VIX1DayPercentSlope'] = 0
            
        # calc VIX best fit
        for numPeriods in bestFitNumPeriods:
            if i >= numPeriods:
                tradingDays[i]['VIX' + str(numPeriods) + 'DaySlope'] = Statistics.findBestFitSlope(tradingDays, i - (numPeriods - 1), i, 'Period', 'VIXClose')
            else:
                tradingDays[i]['VIX' + str(numPeriods) + 'DaySlope'] = 0
        
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


numTrades = 0
totalReturn = 1
lastAction = 'SELL'
firstBuyEncountered = False
firstBuyDate = ''
lastSellDate = ''
lastBuyPrice = 1
lastSellPrice = 1
numTransactions = 0
numPositiveTransactions = 0

#determine buy and sell signals
print('Determining Buy/Sell signals...')
for m, tradingDay in enumerate(tradingDays):
    actionToPerform = 'HOLD'
    
    '''
    ### ORIGINAL BUY ###
    if (m > 0 and 
        tradingDays[m]['SlowSto1DaySlope'] > 0 and 
        tradingDays[m]['VIX1DaySlope'] < 0 and
        tradingDays[m]['AD3DaySlope'] > 0
       ):
        actionToPerform = 'BUY'
    '''
    '''
    ### RSI BUY ###
    if (m > 0 and 
        tradingDays[m]['14DayRSI1DaySlope'] > 1 and 
        tradingDays[m]['VIX1DaySlope'] < -0.2 and
        tradingDays[m]['AD3DaySlope'] > 0
       ):
        actionToPerform = 'BUY'
    '''
    
    ### BOTH BUY ###
    if (m > 0 and 
        tradingDays[m]['SlowSto1DaySlope'] > 0.7 and
        tradingDays[m]['14DayRSI1DaySlope'] > 0.7 and 
        tradingDays[m]['VIX1DaySlope'] < -0.5 and
        tradingDays[m]['AD3DaySlope'] > 0
       ):
        actionToPerform = 'BUY'
    
    '''
    ### ORIGINAL SELL ###
    if (m > 0 and 
        (
         ( #gradual declines
          #tradingDays[m]['SlowSto1DaySlope'] < -3 and 
          tradingDays[m]['VIX1DaySlope'] > 0.5 and
          tradingDays[m]['SlowSto1DayPercentSlope'] < -3 and 
          #tradingDays[m]['VIX1DayPercentSlope'] > 2.5 and
          #tradingDays[m]['AD5DaySlope'] < 0
          (tradingDays[m]['AD5DaySlope'] < 0 or tradingDays[m]['OBV5DaySlope'] < 0)
         ) 
         or
         ( #sharp declines
          tradingDays[m]['SlowSto1DaySlope'] < -5 and 
          #tradingDays[m]['SlowSto3DaySlope'] < 0 and 
          tradingDays[m]['VIX1DaySlope'] > 1.5 and
          #tradingDays[m]['AD5DaySlope'] < 0
          (tradingDays[m]['AD3DaySlope'] < 0 or tradingDays[m]['OBV3DaySlope'] < 0)
         )
        )
       ):
        actionToPerform = 'SELL'
    '''
    '''
    ### RSI SELL ###
    if (m > 0 and 
        (
         ( #gradual declines
          tradingDays[m]['VIX1DaySlope'] > 0.5 and
          tradingDays[m]['14DayRSI1DaySlope'] < -2 and 
          (tradingDays[m]['AD5DaySlope'] < 0 or tradingDays[m]['OBV5DaySlope'] < 0)
         ) 
         or
         ( #sharp declines
          tradingDays[m]['VIX1DaySlope'] > 1.5 and
          tradingDays[m]['14DayRSI1DaySlope'] < -3 and 
          (tradingDays[m]['AD3DaySlope'] < 0 or tradingDays[m]['OBV3DaySlope'] < 0)
         )
        )
       ):
        actionToPerform = 'SELL'
    '''
    
    ### BOTH SELL ###
    if (m > 0 and 
        (
         ( #gradual declines
          tradingDays[m]['VIX1DaySlope'] > 0.4 and
          tradingDays[m]['14DayRSI1DaySlope'] < -2 and 
          tradingDays[m]['SlowSto1DaySlope'] < -2 and
          (tradingDays[m]['AD5DaySlope'] < 0 or tradingDays[m]['OBV5DaySlope'] < 0)
         ) 
         or
         ( #sharp declines
          tradingDays[m]['VIX1DaySlope'] > 1 and
          tradingDays[m]['14DayRSI1DaySlope'] < -4.5 and 
          tradingDays[m]['SlowSto1DaySlope'] < -4.5 and
          (tradingDays[m]['AD3DaySlope'] < 0 or tradingDays[m]['OBV3DaySlope'] < 0)
         )
        )
       ):
        actionToPerform = 'SELL'
    
        
        
    '''
    ### NEW SELL ###
    if (m > 0 and 
        (
         ( #gradual declines
          #tradingDays[m]['SlowSto1DaySlope'] < -3 and 
          tradingDays[m]['SlowSto1DayPercentSlope'] < -3 and 
          tradingDays[m]['VIX1DaySlope'] > 0.5 and
          #tradingDays[m]['VIX1DayPercentSlope'] > 2.5 and
          #tradingDays[m]['AD5DaySlope'] < 0
          (tradingDays[m]['AD5DaySlope'] < 0 or tradingDays[m]['OBV5DaySlope'] < 0)
         ) 
         or
         ( #sharp declines
          tradingDays[m]['SlowSto1DayPercentSlope'] < -5.5 and 
          tradingDays[m]['SlowSto3DaySlope'] < -0.5 and 
          tradingDays[m]['VIX1DayPercentSlope'] > 5.5 and
          #tradingDays[m]['AD5DaySlope'] < 0
          (tradingDays[m]['AD3DaySlope'] < 0 or tradingDays[m]['OBV3DaySlope'] < 0)
         )
        )
       ):
        actionToPerform = 'SELL'
    '''
    
    if lastAction == 'SELL' and actionToPerform == 'BUY':
        if not firstBuyEncountered:
            firstBuyEncountered = True
            firstBuyDate = tradingDay['Date']
            
        #lastBuyPrice = tradingDay['Close']
        lastBuyPrice = (tradingDay['High'] + tradingDay['Low']) / 2
        lastAction = 'BUY'
        numTransactions = numTransactions + 1
    elif lastAction == 'BUY' and actionToPerform == 'SELL':
        #lastSellPrice = tradingDay['Close']
        lastSellPrice = (tradingDay['High'] + tradingDay['Low']) / 2
        totalReturn = totalReturn * lastSellPrice / lastBuyPrice
        lastAction = 'SELL'
        numTransactions = numTransactions + 1
        lastSellDate = tradingDay['Date']
        
        if lastSellPrice > lastBuyPrice:
            numPositiveTransactions = numPositiveTransactions + 1
        
    tradingDays[m]['Buy/Sell'] = actionToPerform
    
    #if m % 10 == 0:
    #    print("      Date      Last       Vol    VIX  1D%Slope  Stoch  1D%Slope  3DaySlope        OBV  3DaySlope  5DaySlope         AD  3DaySlope  5DaySlope  Buy/Sell")

    #print(f"{tradingDay['Date']}  {'%8.2f' % tradingDay['Close']}  {'%.2e' % tradingDay['Volume']}  {'%5.2f' % tradingDay['VIXClose']}  {'%8.2f' % tradingDay['VIX1DayPercentSlope']}  {'%5.2f' % tradingDay['SlowStochastic']}  {'%8.2f' % tradingDay['SlowSto1DayPercentSlope']}  {'%9.1f' % tradingDay['SlowSto3DaySlope']}  {'%9.2e' % tradingDay['OBV']}  {'%9.2e' % tradingDay['OBV3DaySlope']}  {'%9.2e' % tradingDay['OBV5DaySlope']}  {'%9.2e' % tradingDay['AD']}  {'%9.2e' % tradingDay['AD3DaySlope']}  {'%9.2e' % tradingDay['AD5DaySlope']}  {tradingDay['Buy/Sell'].rjust(8)}")

    if m % 10 == 0:
        print("      Date     Last      Vol   VIX 1D%Slope 14DRSI 1DSlope 3DaySlope Stoch 1D%Slope 3DaySlope       OBV 3DaySlope 5DaySlope        AD 3DaySlope 5DaySlope Buy/Sell")

    print(f"{tradingDay['Date']} {'%8.2f' % tradingDay['Close']} {'%.2e' % tradingDay['Volume']} {'%5.2f' % tradingDay['VIXClose']} {'%8.2f' % tradingDay['VIX1DayPercentSlope']} {'%6.2f' % tradingDay['14DayRSI']} {'%7.2f' % tradingDay['14DayRSI1DaySlope']} {'%9.1f' % tradingDay['14DayRSI3DaySlope']} {'%5.2f' % tradingDay['SlowStochastic']} {'%8.2f' % tradingDay['SlowSto1DayPercentSlope']} {'%9.1f' % tradingDay['SlowSto3DaySlope']} {'%9.2e' % tradingDay['OBV']} {'%9.2e' % tradingDay['OBV3DaySlope']} {'%9.2e' % tradingDay['OBV5DaySlope']} {'%9.2e' % tradingDay['AD']} {'%9.2e' % tradingDay['AD3DaySlope']} {'%9.2e' % tradingDay['AD5DaySlope']} {tradingDay['Buy/Sell'].rjust(8)}")





print('First Buy Date:' + firstBuyDate)
print('Last Sell Date:' + lastSellDate)
print('Total Return:' + str(totalReturn))
print('Annual Return:' + str(totalReturn ** (1 / 12)))
print('Num transactions:' + str(numTransactions))
print('Num sells:' + str(numTransactions / 2))
print('Num positive sells:' + str(numPositiveTransactions))
print('Num negative sells:' + str(numTransactions / 2 - numPositiveTransactions))
print('Percent positive sells:' + str(100 * numPositiveTransactions / (numTransactions / 2)))




'''
keys = tradingDays[0].keys()
with open('C:/temp/flashBackup/_stocks/WithVix.csv', 'w', newline = '') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(tradingDays)
'''

