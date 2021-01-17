from oddysey.utils import *
from oddysey.utils import *

class className:
    def __init__(self):
        pass

    def main(self, config, lock):
        # algorithm logic
        lock.release()
        return

if __name__ == '__main__':

    # init thread
    targetCol = 'params_collection'
    main = className()
    Q = {} # filter

    try:
        threadManager(main, targetCol, Q)
        
    except Exception as e:
        print(e)
        sys.exit()
