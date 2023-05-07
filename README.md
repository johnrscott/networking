# Network discovery with Scapy

Install scapy with 

```bash
python3 -m venv venv
source venv/bin/activate
pip install scapy matplotlib cryptography
```

## IP packets

Run `scapy` to get the interactive terminal, and run

```python
>>> raw(IP())
>>> IP(_)
<IP  version=4 ihl=5 tos=0x0 len=20 id=1 flags= frag=0 ttl=64 proto=hopopt chksum=0x7ce7 src=127.0.0.1 dst=127.0.0.1 |>
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
```

