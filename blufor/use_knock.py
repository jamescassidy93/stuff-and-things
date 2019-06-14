import socket
import sys
import time

def usage():
    print("Usage: use_knock.py [server ip] [port sequence]")
    sys.exit(0)

def main():
    if(len(sys.argv)<3):
        usage()
    ip = sys.argv[1]
    seq = sys.argv[2:]
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    for port in seq:
        s.sendto('',(ip,int(port)))
        time.sleep(.2)
    print("Knock sequence complete. You can try to login now.")

if(__name__ == '__main__'):
    main()