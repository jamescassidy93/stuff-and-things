import sys
import socket

def usage():
    print("Usage: use_key.py [path to keyfile] [server ip] [server port]")
    sys.exit(0)

def main():
    if(len(sys.argv)!=4):
        usage()
    key_path = sys.argv[1]
    ip = sys.argv[2]
    port = int(sys.argv[3])
    file = open(key_path)
    key = file.read()
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.sendto(key.encode(),(ip,port))
    print("Key sent. You can try to login now.")

if(__name__ == '__main__'):
    main()