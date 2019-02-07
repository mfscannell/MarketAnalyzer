import Statistics

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
        
def calcRsi(tradingDays, index, numPeriods):
    if index == 0:
        tradingDays[index]['Gain'] = 0
        tradingDays[index]['Loss'] = 0
        tradingDays[index][f"{numPeriods}DayAvgGain"] = 0
        tradingDays[index][f"{numPeriods}DayAvgLoss"] = 0
        tradingDays[index][f"{numPeriods}DayRelativeStrength"] = 0
        tradingDays[index][f"{numPeriods}DayRSI"] = 0
    else:
        if tradingDays[index]['Close'] > tradingDays[index - 1]['Close']:
            tradingDays[index]['Gain'] = tradingDays[index]['Close'] - tradingDays[index - 1]['Close']
            tradingDays[index]['Loss'] = 0
        else:
            tradingDays[index]['Gain'] = 0
            tradingDays[index]['Loss'] = tradingDays[index - 1]['Close'] - tradingDays[index]['Close']
            
        if index < numPeriods:
            tradingDays[index][f"{numPeriods}DayAvgGain"] = 0
            tradingDays[index][f"{numPeriods}DayAvgLoss"] = 0
            tradingDays[index][f"{numPeriods}DayRelativeStrength"] = 0
            tradingDays[index][f"{numPeriods}DayRSI"] = 0
        elif index == numPeriods:
            tradingDays[index][f"{numPeriods}DayAvgGain"] = Statistics.findSimpleAverage(tradingDays, index - (numPeriods - 1), index, 'Gain')
            tradingDays[index][f"{numPeriods}DayAvgLoss"] = Statistics.findSimpleAverage(tradingDays, index - (numPeriods - 1), index, 'Loss')
            
            if tradingDays[index][f"{numPeriods}DayAvgLoss"] > 0:
                tradingDays[index][f"{numPeriods}DayRelativeStrength"] = tradingDays[index][f"{numPeriods}DayAvgGain"] / tradingDays[index][f"{numPeriods}DayAvgLoss"]
                tradingDays[index][f"{numPeriods}DayRSI"] = 100 - 100 / (1 + tradingDays[index][f"{numPeriods}DayRelativeStrength"])
            else:
                tradingDays[index][f"{numPeriods}DayRelativeStrength"] = 1000000
                tradingDays[index][f"{numPeriods}DayRSI"] = 100 - 100 / (1 + tradingDays[index][f"{numPeriods}DayRelativeStrength"])
        else:
            a = tradingDays[index - 1][f"{numPeriods}DayAvgGain"]
            b = tradingDays[index]['Gain']
            tradingDays[index][f"{numPeriods}DayAvgGain"] = ((numPeriods - 1) * a + b) / numPeriods
            tradingDays[index][f"{numPeriods}DayAvgLoss"] = ((numPeriods - 1) * tradingDays[index - 1][f"{numPeriods}DayAvgLoss"] + tradingDays[index]['Loss']) / numPeriods
    
            if tradingDays[index][f"{numPeriods}DayAvgLoss"] > 0:
                tradingDays[index][f"{numPeriods}DayRelativeStrength"] = tradingDays[index][f"{numPeriods}DayAvgGain"] / tradingDays[index][f"{numPeriods}DayAvgLoss"]
                tradingDays[index][f"{numPeriods}DayRSI"] = 100 - 100 / (1 + tradingDays[index][f"{numPeriods}DayRelativeStrength"])
            else:
                tradingDays[index][f"{numPeriods}DayRelativeStrength"] = 1000000
                tradingDays[index][f"{numPeriods}DayRSI"] = 100 - 100 / (1 + tradingDays[index][f"{numPeriods}DayRelativeStrength"])
        

        
        
        
        