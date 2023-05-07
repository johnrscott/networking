# Network discovery with Scapy

Install scapy with 

```bash
sudo apt install python3-scapy
```

## IP packets

Run `scapy` to get the interactive terminal, and run

```python
>>> raw(IP())
>>> IP(_)
<IP  version=4 ihl=5 tos=0x0 len=20 id=1 flags= frag=0 ttl=64 proto=hopopt chksum=0x7ce7 src=127.0.0.1 dst=127.0.0.1 |>

# You can pretty-print a packet using show()
>>> p = IP()
>>> p.show()
###[ IP ]### 
  version= 4
  ihl= None
  tos= 0x0
  len= None
  id= 1
  flags= 
  frag= 0
  ttl= 64
  proto= hopopt
  chksum= None
  src= 127.0.0.1
  dst= 127.0.0.1
  \options\
```

The fields are listed in the order they are present in an IP packet. An IP packet contains two parts: a header (at least 20 octets) and a data section. 

### IP Packet Header

The header contains the following fields:

- **Version** (4 bits): the version of the internet protocol; always equal to 4 for IPv4.
- **Internet header length** (4 bits): the length of the IP packet header in 4-octet words. A length of 5 is usual (meaning 20 octets), when the options field is empty. The maximum header length is 15 (60 bytes).

The TOS (type of service) field (the old name) is split into two fields:
- **Differentiated services code point** (6 bits): used to provide some information about what a packet is being used for; for example, to provide low-latency for (e.g.) real-time services (see RFC 2474 for more information)
- **Explicit congestion notification** (2 bits) used to indicate network congestion if both ends of the connection support it (optional, 00 if not supported; see RFC 3168 for more information).

- **Total length** (16 bits): the length of the entire packet, including both the header and the data, in octets.

- **Identification**: a packet ID, used to identify the group of fragments of a signel (fragmented) IP packet.

- **Flags** (3 bits): Contains (in order) a reserved-zero bit; the DF (do not fragment) flag; and the MF (more fragments) flag. *Do not fragment* will cause a packet that needs to be fragmented to be dropped. *More fragments* is used when a packet is part of a fragmented group: all fragments except the last have the flag set.

- **Fragment offset** (13 bits): the offset to the data contained in the current fragment, in units of 8 octets, relative to the start of the original data payload. Fragmentation is performed to reduce the (total) size of a packet to below the *maximum transfer unit* (MTU) at the data-link layer (e.g. for transmission by ethernet frames). A receiver knows a packet has been fragmented if the *fragment offset* field is non-zero, or the *more fragments* flag is set. Since this field is a multiple of 8 octets, each fragment must begin on an 8-octet-aligned boundary.

- **Time to live** (8 bits): the number of hops (while being routed) that the packet is allowed to undergo before it is dropped. Protects the network against routing loops or related issues.

- **Protocol** (8 bits): the format of the data payload. The IP packet data payload encapsulates protocols at higher levels of the internet protocol stack, including *TCP* (identified by `protocol == 6`), *ICMP* (`protocol == 2`), and *UDP* (`protocol == 17`). 

- **Header checksum** (32 bits): checksum of the IP packet header. The checksum is verified at each router (which must also recalculate the checksum when it decrements *TTL*). If a checksum check fails, the packet is dropped. The data field of the IP packet is not covered by the checksum; that is the responsibility of the protocol encapsulated by the IP packet.

- **Source IP address** (32 bits): the IP address of the host that is apparently sending this IP packet (may not be the real host, due to *network address translation*).

- **Destination IP address** (32 bits): the IP address where the IP packet should be sent. The destination defines how the IP packet is routed (at each hop, a host either forwards the packet to the final destination on one of its local networks, or it sends the packet to a gateway (another host) according to the value in this destination IP address field.

- **Options** (0 bits - 40 bits): miscellaneous packet options; often not used. If options are present, they are concatenated into this *options* field, and padded to a multiple of four octets.

### IP Packet Data Payload

The data payload begins after the packet header, and can be up to 65516 octets to 65496 octets depending on whether the size of the packet header (i.e. the entire packet must not exceed 2^16 = 65536 octets in length). Many packets are much smaller to avoid fragmentation (the process of dividing packets up to conform to the link-layer MTU).

The format of the data payload is defined in the *protocol* header field, and may be *TCP*, *UDP*, *ICMP*, etc. To make a simple IP packet with TCP data, use

```python
# / is the composition (pipe) operator in scapy
>>> IP()/TCP()
<IP  frag=0 proto=tcp |<TCP  |>>

# Full output
>>> p = IP()/TCP()
>>> p.show()
###[ IP ]### 
  version= 4
  ihl= None
  tos= 0x0
  len= None
  id= 1
  flags= 
  frag= 0
  ttl= 64
  proto= tcp
  chksum= None
  src= 127.0.0.1
  dst= 127.0.0.1
  \options\
###[ TCP ]### 
     sport= ftp_data
     dport= http
     seq= 0
     ack= 0
     dataofs= None
     reserved= 0
     flags= S
     window= 8192
     chksum= None
     urgptr= 0
     options= []
```

Some common protocols are described briefly below

#### Internet control message protocol (ICMP)

The ICMP protocol is used to relay information such as error messages between hosts. It is often received as the reply following another operation, and are sent to the source IP of the originating packet. The ICMP format contains a header, containing a *type* and *code* field that together specify the message. This encodes familiar responses such as *Destination host unreachable* or other responses used by other operations (such as *echo request* used for ping). 

To create an ICMP packet in scapy with default values, run:

```python
>>> raw(ICMP())
>>> ICMP(_)
<ICMP  type=echo-request code=0 chksum=0xf7ff id=0x0 seq=0x0 |>
```

#### Transmission control protocol (TCP)

The main data transmission protocol of the internet; packets are delivered with acknowledgement, so the sender is aware the transmission succeeded (the protocol is *reliable*). The TCP protocol establishes a pipe-like data transfer path between two hosts, that is opened using a multi-step TCP handshake and closed in a similar fashion.

To create a TCP packet in scapy, run:

```python
>>> raw(TCP())
>>> TCP(_)
<TCP  sport=ftp_data dport=http seq=0 ack=0 dataofs=5 reserved=0 flags=S window=8192 chksum=0x0 urgptr=0 |>
```

### Sending IP packets

You need root privileges to send packets, so run `sudo scapy` to open the shell. A simple packet to send is the *echo request* (using ICMP), which is a ping.

```python
# To send without receiving
>>> p = IP(dst="192.168.1.190")/ICMP()
>>> p.show()
###[ IP ]### 
  version= 4
  ihl= None
  tos= 0x0
  len= None
  id= 1
  flags= 
  frag= 0
  ttl= 64
  proto= icmp
  chksum= None
  src= 192.168.1.210
  dst= 192.168.1.190
  \options\
###[ ICMP ]### 
     type= echo-request
     code= 0
     chksum= None
     id= 0x0
     seq= 0x0

# To send without receiving
>>> send(p)
Sent 1 packets

# To send and receive
>>> r = sr1(p)  

# View the response
>>> r.show()
###[ IP ]### 
  version= 4
  ihl= 5
  tos= 0x0
  len= 28
  id= 2681
  flags= 
  frag= 0
  ttl= 64
  proto= icmp
  chksum= 0xeb87
  src= 192.168.1.190
  dst= 192.168.1.210
  \options\
###[ ICMP ]### 
     type= echo-reply
     code= 0
     chksum= 0xffff
     id= 0x0
     seq= 0x0
```

A more complex example is a simple web request. For this to work, install apache2 on a target host (for example a raspberry pi), and make not configuration changes (so that the default apache2 page is accessible on port 80). Use a browser to double check the webserver is accessible (`http://192.168.1.190`). Then, perform the following steps (the TCP handshake) as described [here](https://stackoverflow.com/questions/4750793/python-scapy-or-the-like-how-can-i-create-an-http-get-request-at-the-packet-leve)

```python
>>> syn = IP(dst="192.168.1.190") / TCP(dport=80, flags='S')
>>> syn.show()
###[ IP ]### 
  version= 4
  ihl= None
  tos= 0x0
  len= None
  id= 1
  flags= 
  frag= 0
  ttl= 64
  proto= tcp
  chksum= None
  src= 192.168.1.210
  dst= 192.168.1.190
  \options\
###[ TCP ]### 
     sport= ftp_data
     dport= http
     seq= 0
     ack= 0
     dataofs= None
     reserved= 0
     flags= S
     window= 8192
     chksum= None
     urgptr= 0
     options= []

# Receive SYN acknowledgement (note the SA flag)
>>> syn_ack = sr1(syn)
###[ IP ]### 
  version= 4
  ihl= 5
  tos= 0x0
  len= 44
  id= 0
  flags= DF
  frag= 0
  ttl= 64
  proto= tcp
  chksum= 0xb5eb
  src= 192.168.1.190
  dst= 192.168.1.210
  \options\
###[ TCP ]### 
     sport= http
     dport= ftp_data
     seq= 3955460934
     ack= 1
     dataofs= 6
     reserved= 0
     flags= SA
     window= 64240
     chksum= 0xa0d5
     urgptr= 0
     options= [('MSS', 1460)]

# Now perform the request
>>> get_string = 'GET / HTTP/1.1\r\nHost: 192.168.1.190\r\n\r\n'
>>> req = IP(dst="192.168.1.190") / TCP(dport=80, sport=syn_ack[TCP].dport,
             seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / get_string
reply = sr1(req)

```
