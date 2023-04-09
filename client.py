import socket
from threading import Thread


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('62.113.100.8', 50007))


def get_msg():
    done = False
    while not done:
        try:
            msg = sock.recv(1024).decode('utf-8')
        except Exception:
            done = True
            print('d')
        if msg == '1: quit':
            done = True
            sock.close()
        else:
            print(msg)


def send_msg():
    done = False
    while not done:
        msg = input()
        if msg == 'quit':
            done = True
            sock.send(msg.encode('utf-8'))

            sock.close()
        else:
            sock.send(msg.encode('utf-8'))


send = Thread(target=send_msg)
rec = Thread(target=get_msg)
send.start()
rec.start()
send.join()
rec.join()
