import pickle
import DataCollection.Stock as Stock
import DataCollection.ImportData as ImportData




def main(): 
    importDataObject = ImportData.CreateDataSet()
    tickers = ["tsla", "aapl", "spy", "amd","xom"]
    importDataObject.addTickers(tickers)
    theStonks = importDataObject.returnData()


main()