import calendar
import os
import socket
import sys
from datetime import date
from threading import Thread
from time import gmtime, strftime
from typing import Mapping

import requests


class MockServer:
    def __init__(self, output_map: Mapping[str, str], port: int = 80):
        self.output_map = output_map
        self.output_map['/stop'] = "Mock Server Closed!"

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.server.bind(('127.0.0.1', port))

    def respond(self, address):
        address = address.split("?")[0]
        response = self.output_map.get(address)
        response_len = 0
        if response:
            response_len = len(response)

        current_date = calendar.day_abbr[date.today().weekday(
        )]+", "+date.today().strftime("%d %b %Y")+strftime(" %H:%M:%S", gmtime()) + " GMT"

        success = f"""HTTP/1.1 200 OK
Date: {current_date}
Server: Apache/2.2.14 (Win32)
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Length: {80 + response_len}
Content-Type: text/html
Connection: Closed\n\n"""

        failure = f"""HTTP/1.1 404 Not Found
Date: {current_date}
Server: Apache/2.2.14 (Win32)
Content-Length: 230
Connection: Closed
Content-Type: text/html; charset=iso-8859-1\n"""

        if response:
            return success + response
        return failure

    def run(self):
        print(f"Server running: http://127.0.0.1:{self.port}")

        backlog = 10
        self.server.listen(backlog)

        while True:
            try:
                client_sock, client_addr = self.server.accept()
                data = client_sock.recv(2048)

                first_line = data.decode().split('\n')[0]
                address = first_line.split(" ")[1]

                response = self.respond(address)
                
                client_sock.send(response.encode('ascii'))
                client_sock.close()

                if address == "/stop":                    
                    break

            except KeyboardInterrupt:
                print("Good bye!")
                break

        sys.exit()

    def start(self):
        thread = Thread(target=self.run)
        thread.start()
    
    def stop(self):        
        res = requests.get('http://127.0.0.1/stop')
        print(res.text)        


if __name__ == "__main__":
    base_dir = os.path.split(__file__)[0]

    mapping = {}
    with open(os.path.join(base_dir, 'templates/lvl_1.html')) as f:
        mapping['/'] = f.read()

    with open(os.path.join(base_dir, 'templates/lvl_2.html')) as f:
        mapping['/lvl_2'] = f.read()

    with open(os.path.join(base_dir, 'templates/lvl_3.html')) as f:
        mapping['/lvl_3'] = f.read()

    with open(os.path.join(base_dir, 'templates/lvl_4.html')) as f:
        mapping['/lvl_4'] = f.read()

    server = MockServer(mapping)
    server.start()
