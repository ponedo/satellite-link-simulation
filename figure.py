import time
import re
import matplotlib.pyplot as plt
import numpy as np

def timestr_to_timestamp(timestr):
    return time.mktime(time.strptime(timestr, "%Y-%m-%d %H:%M:%S"))


def draw_figure(file_suffix):
    f_ls = "./log/link_state_log_" + file_suffix
    f_tr = "./log/transmission_log_" + file_suffix

    # read link_state data
    timestr, bw, delay, loss = [], [], [], []
    with open(f_ls, 'r') as f:
        for line in f:
            line = line.strip()
            tstr, b, d, l, c = line.split("\t")
            timestr.append(tstr)
            bw.append(int(b))
            try:
                delay.append(int(d[:-2]))
            except:
                delay.append(150)
            b = int(l[:-1])
            loss.append(b if b < 10 else 10)    
    ls_timestamp = [timestr_to_timestamp(tstr) for tstr in timestr]
    min_ls_tstamp = min(ls_timestamp)
    ls_timestamp = [tstamp - min_ls_tstamp for tstamp in ls_timestamp]
    scaled_loss = [20 * l for l in loss] # scale by 20x

    # read trasmission_log data
    tr_timestamp, rate = [], []
    with open(f_tr, 'r') as f:
        for line in f:
            line = line.strip()
            l_tstr, u_tstr, byte_n, r = line.split("\t")
            l_tstamp = timestr_to_timestamp(l_tstr)
            u_tstamp = timestr_to_timestamp(u_tstr)
            tstamp = (l_tstamp + u_tstamp) / 2.
            tr_timestamp.append(tstamp)
            r = int(r.split('.')[0])
            rate.append(r)
    min_tr_tstamp = min(tr_timestamp)
    tr_timestamp = [tstamp - min_tr_tstamp for tstamp in tr_timestamp]

    # plot bw, delay, loss and transmit rate
    suffix = re.sub(r'(\d+)', '', file_suffix)
    plt.xlabel("time/s") 
    plt.title("bw, delay, loss and transmit rate for " + suffix.upper())
    plt.plot(ls_timestamp, bw, label='bandwidth', color="lightgreen", linestyle=":")
    plt.plot(ls_timestamp, delay, label='delay', color="pink", linestyle=":")
    plt.plot(ls_timestamp, scaled_loss, label='loss(scaled by 20x)', color="cyan", linestyle=":")
    plt.plot(tr_timestamp, rate, label='rate', color="red", linestyle="-")
    plt.legend(loc='upper right')
    plt.savefig("./figure/" + suffix + ".jpg")
    plt.close()


def draw_rate_cmp_figure(file_suffixes):
    color_arr = ["lightblue", "lightgreen", "red", "gold"]
    linestyle_arr = [':', ':', '-', '-']

    for color, linestyle, file_suffix in zip(color_arr, linestyle_arr, file_suffixes):
        f_tr = "./log/transmission_log_" + file_suffix
        tr_timestamp, rate = [], []
        with open(f_tr, 'r') as f:
            for line in f:
                line = line.strip()
                l_tstr, u_tstr, byte_n, r = line.split("\t")
                l_tstamp = timestr_to_timestamp(l_tstr)
                u_tstamp = timestr_to_timestamp(u_tstr)
                tstamp = (l_tstamp + u_tstamp) / 2.
                tr_timestamp.append(tstamp)
                r = int(r.split('.')[0])
                rate.append(r)
        min_tr_tstamp = min(tr_timestamp)
        tr_timestamp = [tstamp - min_tr_tstamp for tstamp in tr_timestamp]

        suffix = re.sub(r'(\d+)', '', file_suffix)
        plt.plot(tr_timestamp, rate, label=suffix+' rate', color=color, linestyle=linestyle)

    plt.legend(loc='upper right')
    plt.savefig("./figure/cmp.jpg")
    plt.close()


if __name__ == "__main__":
    file_suffixes = ["reno", "cubic", "bbr1", "mybbr10"]
    draw_rate_cmp_figure(file_suffixes)
    for file_suffix in file_suffixes:
        draw_figure(file_suffix)