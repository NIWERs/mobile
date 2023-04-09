import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('0.0.0.0', 4144))

sock.listen(1)


k = 0
ls = []
msg = ''

while 2 != k:
    con, add = sock.accept()
    ls.append([con, add])
    k += 1
    print(add)

done = False

while True:
    msg = ls[1][0].recv(1024).decode('utf-8')
    print(msg)
    ls[0][0].sendall(f'2:{msg}'.encode('utf-8'))
    msg_1 = ls[0][0].recv(1024).decode('utf-8')

    ls[1][0].sendall(f'1:{msg_1}'.encode('utf-8'))

