# Wireshark 

Install on Ubuntu 22.04 as follows:

```bash
sudo apt install wireshark-qt
# Run wireshark
sudo wireshark
```

## Capturing packets

After opening wireshark, type `host 192.168.1.233` (the target host whose packets are desired) into the capture filter window. Then click on the desired interface and type `C-e` to start logging packets. Press `C-e` again to stop.

A simple way to test the capturing is working is to ping the host. Start capturing, and run `ping -c 3 192.168.1.233`. You should see 6 ICMP packets (3 echo requests and 3 echo replies).

A more complex example is a TCP connection. First, set up the following capture filter to restrict to TCP traffic destined for a particular port: `host 192.168.1.233 and tcp port 7878`. Next, start capturing, and run the following `netcat` to try to send data to port `7878` on `192.168.1.233`:

```bash
nc 192.168.1.233 7878
```

Wireshark should show two packets: a `SYN` transmitted to `192.168.1.233`, following by a `RST`, indicating that port `7878` is not listening. Now, start listening on port 7878 by running the following netcat command on `192.168.1.233`:

```bash
# Choose a port above 1023 to avoid using root
nc -l 7878
```

Now, running `nc` on the client should successfully connect, and it should be possible to send data.

```bash
nc 192.168.1.233 7878
```

In this case, the first SYN packet is followed by a SYN acknowledgement, rather than a RST acknowledgement. The handshake completes after a third ACK packet is sent to 192.168.1.233.

With the `netcat` connection still open, send text by typing `Hi` at `stdin`. Pressing enter triggers a send, which consists of two packets, the first containing the text `Hi` in the data field of the TCP payload, and the second (returned from the server) containing an ACK (confirming reception). 

To simulate transmission errors, put a firewall in place after the connection has been established, by running:

```bash
sudo ufw allow 22
sudo ufw enable
```

(This assumes the firewall was previously disabled). The client/server do not realise anything is wrong until the client tries to send a packet. Since the data never reaches the server, no ACK is sent, and the client will keep retrying, with progressively longer delays between tries. If the firewall is disabled during this period, the transmission will conclude successfully as normal.


