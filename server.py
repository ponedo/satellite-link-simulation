from socket import *
import argparse
from time import ctime

print("TCP server starts")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--ip', '-i', 
        default="10.0.0.1", 
        dest='ip',
        help='IP address of server.')
    args = parser.parse_args()
    return args
args = parse_args()


# HOST = ''
HOST = args.ip
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('...connnecting from:', addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ)
        if data == "byebye":
            break
        # if not data:
        #     break
        #tcpCliSock.send('[%s] %s' %(bytes(ctime(),'utf-8'),data))
        # tcpCliSock.send(('[%s] %s' % (ctime(), data)).encode())
    tcpCliSock.close()
    break
tcpSerSock.close()