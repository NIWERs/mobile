from threading import Thread
from multiprocessing import Process, Pipe
import time

class Exchange(Process):
    def __init__(self, sock, conn, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = conn
        self.sock = sock
        self.done = False
        self.c = 'dd'

    def run(self):
        self.sock.connect(('62.113.100.8', 50007))
        t1 = Thread(target=self.send_msg, kwargs=dict(conn=self.conn))
        t2 = Thread(target=self.get_msg, kwargs=dict(conn=self.conn))
        t1.start()
        t2.start()
        print('dd')
        t1.join()
        print('cocaina')

        t2.join()
        print('ddssax')

    def get_msg(self, conn):
        while not self.done:
            print(self.done)
            self.c += 's'
            msg = self.sock.recv(1024).decode('utf-8')
            print(msg)
            if msg == '/quit':
                self.done = True
                time.sleep(2)
                self.sock.send('/quit'.encode('utf-8'))

            else:
                conn.send(msg)

    def send_msg(self, conn):
        while not self.done:
            msg = conn.recv()
            print(self.c)
            if msg == '/quit':
                self.done = True
                self.sock.send(msg.encode('utf-8'))
            else:
                self.sock.send(msg.encode('utf-8'))
