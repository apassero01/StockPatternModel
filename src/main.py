from ast import pattern
import pickle
import DataCollection.Stock as Stock
import DataCollection.ImportData as ImportData
import PriceAnalysis.FindPatterns as Patterns




def main(): 
    # importDataObject = ImportData.CreateDataSet()
    
    # tickers = importDataObject.getTickers()
    # importDataObject.addTickers(tickers)
    # theStonks = importDataObject.returnData()
    # importDataObject.clearBadTicks()
   
    # importDataObject.updateTickers()
    # theStonks = importDataObject.returnData()

    # print(theStonks["tsla"].priceData)
    testOneStock("aapl")


def testOneStock(stock):
    
    stockobj = Stock.StockObject(stock)
    stockobj.initializeData('2020-01-01')
    patternFinder = Patterns.FindPatterns(stockobj)
    patternFinder.analyzePriceData()

    for resistance in patternFinder.resistance:
        print(resistance)
    


    

main()