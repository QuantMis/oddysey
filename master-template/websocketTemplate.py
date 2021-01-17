import json, websocket, _thread

class className:
    def __init__(self):
        self.uri = f"some_streaming_uri"

        try:
            self.ws = websocket.create_connection(self.uri)
        except Exception as e:
            print(e)
            logging.error("fail to establish ws connection")
            return

        _thread.start_new_thread(self.run, ())

    
    def updateOB(self, params, lock):
        # your algorithm
        lock.release()
        return

    def updateTrades(self, params, lock):
        # your algorithm
        lcok.release()
        return


    
    def run(self):
        try:
            msg = json.loads(self.ws.recv())
        except Exception as e:
            print(e)
            self.ws = websocket.create_connection(self.uri)
            msg = json.loads(self.ws.recv())

        if self.ws.connected:

            # parsing different msg type differs based on stream 
            # but in terms of parsing and storing into db 
            # mostly the flow is like this bah
            
            if msg['data']['e']=="depthUpdate":
                lock = _thread.allocate_lock()
                lock.acquire()
                _thread.start_new_thread(self.updateOB, ('bids', msg['data']['b'], lock))
                lock = _thread.allocate_lock()
                lock.acquire()
                _thread.start_new_thread(self.updateOB, ('asks', msg['data']['a'], lock))
            
            elif msg['data']['e']=="aggTrade":
                lock = _thread.allocate_lock()
                lock.acquire()
                _thread.start_new_thread(self.updateTrades, (msg['data'], lock))

        return


if __name__ == '__name__':

    # init websocket
    try:
        while True:
            className()

    except Exception as e:
        print(e)
        sys.exit(0)
