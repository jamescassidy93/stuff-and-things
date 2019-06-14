import sys
import os
import time
import datetime
import threading
import signal
import OpenSSL
import socket
import optparse

from scapy.all import *

SERV_IP = '127.0.0.1'
SERV_KEY_PORT = 3393

# Utility functions

def usage():
    print("Usage: door.py --cert [path to public key] --ports [list of ports]")
    sys.exit(0)

def log(message):
    log = open("door.log","a+")
    log.write("[" + str(datetime.datetime.now()) + "] "+message+'\n')
    log.close()

def check_seq(seq):
    for port in seq:
        if(int(port)<=10000 and int(port)>=40000):
            return False
    return True

def port_seq_callback(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

# Firewall logic

def unlock(ip):
    print("["+str(ip)+"] Door unlocked.")
    #os.system("sudo ufw in from " + str(ip))

def lockandkey(crt_obj):
    while True:
        allow = True
        context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
        context.use_certificate(crt_obj)
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind((SERV_IP,SERV_KEY_PORT))
        key,src_ip = s.recvfrom(4096)
        try:
            key_obj = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
            context.use_privatekey(key_obj)
        except OpenSSL.crypto.Error:
            log("[E]["+str(src_ip[0])+"] Invalid key given. Resetting.")
            continue
        try:
            context.check_privatekey()
        except OpenSSL.SSL.Error:
            allow = False
        if(allow):
            log("["+str(src_ip[0])+"] Key accepted.")
            unlock(src_ip[0])

def knock(seq):
    while True:
        allow = True
        first_knock_port = seq[0]
        first_knock_pkt = sniff(filter="udp dst port "+str(first_knock_port),count=1)
        src_ip = first_knock_pkt[0][IP].src
        log("First knock. Source: " + str(src_ip))
        for port in seq[1:]:
            knock_pkt = sniff(filter="udp and src host "+str(src_ip),count=1,timeout=2)
            if(knock_pkt[0][UDP].dport != int(port) or src_ip != knock_pkt[0][IP].src):
                log("[E]["+str(src_ip)+"] Sequence broken. Resetting.")
                allow = False
                break
            log("["+str(src_ip)+"] Next knock received.")
        if(allow):
            log("["+str(src_ip)+"] Knock accepted.")
            unlock(src_ip)

# main function

def main():
    parser = optparse.OptionParser()
    parser.add_option('--cert',type='string',dest='crt_path')
    parser.add_option('--ports',type='string',action='callback',callback=port_seq_callback,dest='port_seq')
    (options,args) = parser.parse_args()
    if(options.crt_path is None and options.port_seq is None):
        usage()
    if(options.crt_path is not None):
        f = open(options.crt_path)
        crt = f.read()
        try:
            crt = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, crt)
            lockandkey_thread = threading.Thread(target=lockandkey, args=(crt,))
            lockandkey_thread.start()
            log("Door now monitored for key.")
        except OpenSSL.crypto.Error:
            log("[E] Given cert is not in proper PEM format, skipping")
    if(options.port_seq is not None):
        if(len(options.port_seq)>=2 and check_seq(options.port_seq)):
            knock_thread = threading.Thread(target=knock, args=(options.port_seq,))
            knock_thread.start()
            log("Door now monitored for knock. Knock sequence: " + str(options.port_seq))
        else:
            log("[E] Given port sequence is not a valid port sequence, skipping")
    print("Door monitor is here.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log("Door unmonitored. Goodbye.")
        print("\nDoor monitor is gone. Goodbye.")
        os.kill(os.getpid(),signal.SIGKILL)

if __name__ == "__main__":
    main()