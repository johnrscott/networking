# "https://stackoverflow.com/questions/4750793/
#  python-scapy-or-the-like-how-can-i-create-
#  an-http-get-request-at-the-packet-leve"
#
# To stop the kernel from resetting the connection,
# add this iptables rule:
#
# sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -s 192.168.1.233 -j DROP
#
# where the IP is the source IP address of the SYN packet.

from scapy.all import *

syn = IP(dst="192.168.1.233") / TCP(dport=7878, flags='S')
print("SYN packet:")
syn.show()

# Receive SYN acknowledgement (note the SA flag)
syn_ack = sr1(syn)
print("SYN acknowledge:")
syn_ack.show()

# Now perform the request
data = 'Hello World!'
req = IP(dst="192.168.1.233") / TCP(dport=80, sport=syn_ack[TCP].dport,
                                    seq=syn_ack[TCP].ack,
                                    ack=syn_ack[TCP].seq + 1,
                                    flags='A') / data
reply = sr1(req)
reply.show()
