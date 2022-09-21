from datetime import date


class BaseTransaction:
    BUY_FEE = 0.15
    BUY_TAX = 0.01
    SELL_FEE = 0.15
    SELL_TAX = 0.01
    Date: date.today()
    Symbol: str
    
class BuyTransaction(BaseTransaction):
    def save():
        pass

class SellTransaction(BaseTransaction):
    pass

class TransactionBooks:
    def getStocks(self):
        pass

    def insertBuyTransaction(self):
        pass

    def insertSellTransaction(self):
        pass

    def exportTransactionBookToExcel():
        pass



