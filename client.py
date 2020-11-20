import os, time
import argparse
from socket import *

print("TCP client starts")
enter_time = str(int(time.time()))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--test-time', '-t', 
        type=int, 
        default=60, 
        dest='test_time',
        help='Test time in seconds.')
    parser.add_argument(
        '--ip', '-i', 
        default="10.0.0.1", 
        dest='ip',
        help='IP address of server.')
    args = parser.parse_args()
    return args
args = parse_args()

if "log" not in os.listdir("."):
    os.mkdir("./log")

# HOST = '127.0.0.1' # or 'localhost'
HOST = args.ip # or 'localhost'
PORT = 21567
BUFSIZ =1024
ADDR = (HOST,PORT)

tcpCliSock = socket(AF_INET,SOCK_STREAM)
tcpCliSock.connect(ADDR)

start_time = time.time()
snd_bytes = 0
ts = int(time.time())
while True:
    now = int(time.time())
    if now - ts >= 1:
        snd_rate = str(8.*snd_bytes / (1024**2 *(now-ts))) + "Mbps"
        ts_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
        now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
        with open("./log/transmission_log_" + enter_time, 'a') as f:
            f.write("{}\t{}\t{}\t{}\n".format(ts_str, now_str, snd_bytes, snd_rate))
        ts = now
        snd_bytes = 0
    if time.time() - start_time > args.test_time:
        data1 = "byebye"
        break
    else:
        data1 = "aaaaaaaaaaaaaaaaa"
    snd_data = data1.encode()
    tcpCliSock.send(snd_data)
    snd_bytes += len(snd_data)
    # data1 = input('>')
    # data1 = tcpCliSock.recv(BUFSIZ)
    # if not data1:
    #     break
    # print(data1.decode('utf-8'))

tcpCliSock.close()
