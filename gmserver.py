import socket
from _thread import *
import sys
import json

class GameMakerServer:
    def __init__(self, port=5000):
        self.port = port
        self.events = dict()        

    def receive_data(self, conn):
        data = conn.recv(1024)
        if not data:
            return

        print("data received")
        print(data.decode('utf-8'))
        packs = data.decode('utf-8').split('\u0000')
        for pack in packs:
            self.process_pack(pack, conn)        

    def send(self, data, conn):        
        conn.send(json.dumps(data).encode())
        
    def process_pack(self, pack, conn):
        if pack == "":
            return
        self.process_event(json.loads(pack), conn)

    def process_event(self, data, conn):
        print(data["event"])
        self.events[data["event"]](data,conn)

    def threaded_client(self, conn):
        data = {
            "event": "connect"
        }
        self.events["connect"](data, conn)
        print("start listen")    
        while True:
            self.receive_data(conn)
            
        print("Connection Closed")
        conn.close()

    def on_event(self, event, callback):
        self.events[event] = callback

    def run(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = 'localhost'

        try:
            s.bind((server, self.port))
        except socket.error as e:
            print(str(e))
        s.listen(5000)

        print("GameMaker server started")
        print("Listening on port %s" % self.port)

        while True:
            conn, addr = s.accept()
            print("Connected to: ", addr)
            start_new_thread(self.threaded_client, (conn,))