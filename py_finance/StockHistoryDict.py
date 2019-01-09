def toStockDict(stockHistoryString):
    tempTradingDays = stockHistoryString.split('\n')
    tradingDays = []

    keys = tempTradingDays[0].split(',')

    iTradingDays = 1

    while iTradingDays < len(tempTradingDays):
        if tempTradingDays[iTradingDays] != '' and 'null' not in tempTradingDays[iTradingDays]:
            tempTradingDay = tempTradingDays[iTradingDays].split(',')
            tradingDay = {}
            
            tradingDay['Period'] = iTradingDays

            for j, item in enumerate(tempTradingDay):
                if keys[j] == 'Date':
                    tradingDay['Date'] = item
                else:
                    tradingDay[keys[j]] = float(item)

            tradingDays.append(tradingDay)

        iTradingDays = iTradingDays + 1
        
    return tradingDays