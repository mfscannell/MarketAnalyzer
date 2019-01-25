def findSimpleAverage(aList, start, stop, attribute = ''):
    sum = 0
    
    for i in range(start, stop + 1):
        if attribute == '':
            sum = sum + aList[i]
        else:
            sum = sum + aList[i][attribute]
        
    return sum / (stop - start + 1)

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