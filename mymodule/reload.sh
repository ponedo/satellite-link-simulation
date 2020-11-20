sudo sysctl -w net.ipv4.tcp_congestion_control=reno
sudo rmmod "tcp_"$1
sed -i "s/obj-m := .*\.o$/obj-m := tcp_"$1"\.o/g" Makefile
make
sudo insmod "tcp_"$1".ko"
sudo sysctl -w net.ipv4.tcp_congestion_control=$1