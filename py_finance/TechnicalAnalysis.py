# @summary Calculates the On Balance Volume for a trading day in a list of trading days.
# @param tradingDays The list of trading days.
# @param index The index in the list to find the OBV at.
def calcOBV(tradingDays, index):
    if index == 0:
        return tradingDays[index]['Volume']
    elif tradingDays[index]['Close'] > tradingDays[index - 1]['Close']:
        return tradingDays[index - 1]['OBV'] + tradingDays[index]['Volume']
    elif tradingDays[index]['Close'] < tradingDays[index - 1]['Close']:
        return tradingDays[index - 1]['OBV'] - tradingDays[index]['Volume']
    else:
        return tradingDays[index - 1]['OBV']
        
def calcAccumDist(tradingDays, index):
    if index == 0:
        return tradingDays[index]['Volume'] * (
        (tradingDays[index]['Close'] - tradingDays[index]['Low']) - (tradingDays[index]['High'] - tradingDays[index]['Close'])
        ) / (tradingDays[index]['High'] - tradingDays[index]['Low'])
    else:
        return tradingDays[index - 1]['AD'] + tradingDays[index]['Volume'] * (
        (tradingDays[index]['Close'] - tradingDays[index]['Low']) - (tradingDays[index]['High'] - tradingDays[index]['Close'])
        ) / (tradingDays[index]['High'] - tradingDays[index]['Low'])

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
    
def calcSlowStochastic(tradingDays, start, stop):
    lowestLow = findLowestLow(tradingDays, start, stop, 'Low')
    highestHigh = findHighestHigh(tradingDays, start, stop, 'High')
    
    return 100 * (tradingDays[stop]['Close'] - lowestLow) / (highestHigh - lowestLow)
        
        
        
        
        
        
        