from oddysey.sizing import SizingLibrary
config = {"_id":{"$oid":"6002ae10da9a1821df141e9d"},"name":"ethMomentumTest","symbol":"ETHUSDT","sizing_method":"1PCR","account":"testAccount","entryAlgo":"MomentumEntry","exitAlgo":"standardExitAlgo","signal":"eth_momentum"}
a = SizingLibrary(config).returnVal()
print(a)
