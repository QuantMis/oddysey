from oddysey.utils import *
class SizingLibrary:
    def __init__(self, config):
        self.account = initMongo('accountData').find_one({'name':config['account']})
        self.config = config
        self.returnVal()

    def one_percent_risk(self):
        pc = 0.01 
        # add logic later
        return 1

    def returnVal(self):
        if self.config['sizing_method'] == '1PCR':
            return self.one_percent_risk()

        # add elif to return other sizing method

        else:
            # if nothing match, return the safest one
            return self.one_percent_risk()
        

