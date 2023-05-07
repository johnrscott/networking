# "https://stackoverflow.com/questions/4750793/
#  python-scapy-or-the-like-how-can-i-create-
#  an-http-get-request-at-the-packet-leve"

from scapy.all import *

syn = IP(dst="192.168.1.190") / TCP(dport=80, flags='S')
syn.show()

# Receive SYN acknowledgement (note the SA flag)
syn_ack = sr1(syn)
syn_ack.show()

# Now perform the request
get_string = 'GET / HTTP/1.1\r\n\r\n'
req = IP(dst="192.168.1.190") / TCP(dport=80, sport=syn_ack[TCP].dport,
                                    seq=syn_ack[TCP].ack,
                                    ack=syn_ack[TCP].seq + 1,
                                    flags='A') / get_string
reply = sr1(req)
reply.show()
