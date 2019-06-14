import sys
import socket

def usage():
    print("Usage: sscan.py <target IP>")
    sys.exit(0)

def main():
    if(len(sys.argv)!=2):
        usage()
    tip = sys.argv[1]
    phdict = {}
    for port in range(1,1024):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((tip,port))
        except socket.error:
            s.close()
            continue
        try:
            header = s.recv(1024)
        except socket.timeout:
            header = ''
        phdict[port] = header.strip('\n')
        s.close()
    print("Found "+str(len(phdict))+" open ports.")
    for port in sorted(phdict):
        print("Port "+str(port)+": "+phdict[port])

if __name__=='__main__':
    main()