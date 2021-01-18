from oddysey.utils import *

class SizingLibrary:
    def __init__(self, config, signal):
        self.account = initMongo('accountData').find_one({'name':config['account']})
        self.config = config
        self.signal = signal
        self.returnVal()

    def one_percent_risk(self):
        pc = 0.01 
        return 1

    def percentMargin(self):
        trader = self.config
        account = self.account
        marginPerOrder = (trader['maxMargin']/100)/(trader['maxOrderBatch'])
        usdtPerOrder = marginPerOrder*account['inventoryValueUsdt'] 
        qty = usdtPerOrder / getBBO(config['symbol'], signal)
        return qty
        
    def returnVal(self):
        if self.config['sizingMethod'] == '1PCR':
            return self.one_percent_risk()

        elif self.config['sizingMethod'] == 'PERCENT_MARGIN':
            return self.percentMargin()

        else:
            return self.one_percent_risk()
        

