import pickle
import DataCollection.Stock as Stock
import DataCollection.ImportData as ImportData




def main(): 
    importDataObject = ImportData.CreateDataSet()
    # tickers = importDataObject.getTickers()
    # importDataObject.addTickers(tickers)
    # theStonks = importDataObject.returnData()
    # importDataObject.clearBadTicks()
    importDataObject.updateTickers()
    theStonks = importDataObject.returnData()

    print(theStonks["tsla"].priceData)




main()