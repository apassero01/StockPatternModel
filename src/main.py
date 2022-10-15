from ast import pattern
import pickle
import DataCollection.Stock as Stock
import DataCollection.ImportData as ImportData
import PriceAnalysis.FindPatterns as Patterns




def main(): 
    importDataObject = ImportData.CreateDataSet()
    
    # tickers = importDataObject.getTickers()
    # importDataObject.addTickers(tickers)
    # theStonks = importDataObject.returnData()
    # importDataObject.clearBadTicks()
   
    # importDataObject.updateTickers()
    stockList = importDataObject.returnData()
    stock1 = stockList.get("tsla")

    print("The length of the stock list is ", len(stockList))
    print("The amount of price data points for each stock is ", len(stock1.priceData))

    print(stock1.priceData)


    


    # print(theStonks["tsla"].priceData)
    # testOneStock("aapl")


def testOneStock(stock):
    
    stockobj = Stock.StockObject(stock)
    stockobj.initializeData('2020-01-01')
    patternFinder = Patterns.FindPatterns(stockobj)
    patternFinder.analyzePriceData()

    for levels in patternFinder.levels:
        print(levels)
    


    

main()