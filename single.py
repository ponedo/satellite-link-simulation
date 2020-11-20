#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
import threading as thd
import os
import time
import random
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--test-time', '-t', 
        type=int, 
        default=60, 
        dest='test_time',
        help='Test time in seconds.')
    args = parser.parse_args()
    return args
args = parse_args()

enter_time = str(int(time.time()))

class Single(Topo):
    def build(self):
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        self.addLink(h1, h2, bw=100, delay="100ms", loss=1)


def change_link_state():
    h2 = net.get("h2")
    intf = h2.intf()

    # disconnect simulation
    disconnect_prob = 0.05 # randomly disconnect
    disconnect = random.random() < disconnect_prob
    if disconnect:
        # disc_time = random.uniform(0.1, 1)
        disc_time = random.choice([i/10. for i in range(1, 11)])
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        intf.ifconfig("down")
        with open("./log/link_state_log_" + enter_time, 'a') as f:
            conn_state = "DISCONN" if disconnect else "CONN"
            line = "{}\t{}\t{}\t{}%\t{}\n".format(timestamp, "0", "INFms", "100", conn_state)
            f.write(line)
        time.sleep(disc_time)
        intf.ifconfig("up")
        return

    # set new link arguments
    # new_loss = random.choice([i/10. for i in range(1, 11)])
    new_loss = random.choice([i for i in range(1, 6)])
    new_bw = random.randint(100, 200) # new bandwidth
    new_delay = "{}ms".format(random.randint(20, 100)) # new delay

    # change link state
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    intf.config(
        bw=new_bw, 
        delay=new_delay, 
        loss=new_loss, 
        # max_queue_size=500
        )
    
    # record link state change into log
    with open("./log/link_state_log_" + enter_time, 'a') as f:
        conn_state = "DISCONN" if disconnect else "CONN"
        line = "{}\t{}\t{}\t{}%\t{}\n".format(timestamp, new_bw, new_delay, new_loss, conn_state)
        f.write(line)

def change_link_state_thread():
    start_time = time.time()
    while time.time() - start_time < args.test_time:
        print("Link changed!")
        change_link_state()
        stable_time = random.randint(1, 10)
        time.sleep(stable_time)


if __name__ == "__main__":
    if "log" not in os.listdir("."):
        os.mkdir("./log")

    single_topo = Single()
    net = Mininet(topo=single_topo, link=TCLink, controller=None)

    h1_addr, h2_addr = "10.0.0.1", "10.0.0.2"
    h1, h2 = net.get("h1", "h2")
    h1.cmd("ifconfig h1-eth0 " + h1_addr + "/8")
    h2.cmd("ifconfig h2-eth0 " + h2_addr + "/8")
    h1.cmd("sysctl net.ipv4.ip_forward=1")
    h2.cmd("sysctl net.ipv4.ip_forward=1")

    net.start()
    # h1.popen("python server.py -i " + h1_addr)
    # h2.popen("python client.py -i " + h1_addr + " -t " + str(args.test_time - 10))
    CLI(net)
    t = thd.Thread(target=change_link_state_thread) # change link state
    print("Link state is changable!")
    t.start()
    t.join()
    net.stop()