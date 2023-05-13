# Testing setup

Experiments in this repository use a Raspberry Pi 3b+, configured as described in this folder. The raspberry pi is managed by [Ansible](https://docs.ansible.com/ansible/latest/getting_started/index.html), so the configuration is completely defined by the contents of this folder. This makes a repeatable setup that can be recreated the same every time. If you make any manual modifications which break anything, you can just wipe the SD card and start again.

## Setting up the raspberry pi

Download the Raspberry Pi Imager from [here](https://www.raspberrypi.com/software/). Plug an SD (16 GiB) into your computer run:

```bash
sudo rpi-imager
```

For version 1.7.4, follow these steps:

- **Choose OS**: Click `Operating System`, click `Raspberry Pi OS (Other)`, and select `Raspberry Pi OS Lite (64-bit)`. This is the version with no graphics.
- **Pick the SD Card**: Click `Storage` and select the SD card you have plugged in.
- **Configuration**. Click the cog at the bottom right of the screen. Set the hostname to anything (e.g. `rpidev`) that will identify it on the network.
  - Skip down to `Set username and password` and set `user` to `ansible`, with a strong password. 

  - Choose `Allow public key authentication only`. To generate a key, run the following on your computer:
	```bash
	cd ~/.ssh
	ssh-keygen -t ed25519 -f rpidev
	```
	Set a password to encrypt the private key. Use `cat rpidev.pub` to get the contents of the public key, and copy it into the `Set authorized_keys 'ansible'`.
  - Configure wireless networking -- this makes it easier to sniff packets on the wireless interface (which both your laptop and the PI are connected to). 
  - Click save
- **Write**: Click `Write`, confirm wiping all SD card data, and wait for the write and verify to complete.

Take the SD card
