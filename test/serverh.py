import client_http_handler as chh
import requests
import util as ut
import time
import threading

if __name__ == "__main__":
    server=chh.ThreadedHTTPServer(('0.0.0.0', 12345), chh.Resquest)
    chh.server_instance=server

    threading.Thread(target=server.serve_forever,).start()
        # server.serve_forever()

    while True:
        print("结束")
        time.sleep(1)