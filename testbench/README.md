# Configuring a Raspberry Pi for Testing

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
  - Configure wireless networking -- this makes it easier to sniff packets on the wireless interface (which both your computer and the PI are connected to). Use whatever wireless networking your computer is connected to.
  - Click save
- **Write**: Click `Write`, confirm wiping all SD card data, and wait for the write and verify to complete.

While the write is taking place, create a virtual environment for ansible:

```bash
# The ansible configuation is in this folder
cd /this/readme/location
# Install python3 and the virtual environment module
sudo apt install python3 python3-venv
# Make a new virtual environment called venv
python3 -m venv venv 
# Activate the virtual environment and install ansible. Make
# sure you run this before doing any ansible commands
source venv/bin/activate
pip install ansible
# Check ansible is installed correctly
ansible --version
```

Once the SD card has finished writing, take it out the computer, plug it into the raspberry pi. After a few minutes (wait at least 3-5 minutes) it should have booted up, and you should be able to ping it (provided your computer is on the same network as the raspberry pi):

```bash
ping -c3 pibert # -c3 limits to 3 pings
```

If it doesn't work, either the hostname or the wireless configuration may be wrong. Check your router page for whether the raspberry pi is connected or not. If it isn't, redo the SD card and double check the WiFi credentials. If it is, double check the hostname is what you think it is (`rpidev`) -- it may also be resolvable as `ping -c3 rpidev.local`. Get ping working before moving on.

Once the device is reachable at `hostname` (either `rpidev` or `rpidev.local`), test that ansible can reach the raspberry pi:

```bash
# Throughout this readme, {...} should be replaced 
# by the correct value
ansible all -m ping --extra-vars host={hostname}
```

If this works, then the `ansible` user is accessible, and the SSH keypair worked. Set up the raspberry pi by running:

```bash
# Unlock the ssh key for the ansible session (to prevent
# ansible repeatedly asking for the passphrase)
ssh-add ~/.ssh/rpidev
# Configure the raspberry pi
ansible-playbook setup-rpidev.yaml --extra-vars host={hostname}
```

You may want to be able to log in to the raspberry pi yourself. To make this easy, add the following block to your `~/.ssh/config` file:

```conf
Host rpidev
     HostName {hostname}
     IdentitiesOnly yes
     IdentityFile ~/.ssh/rpidev
```

You can now SSH in using `ssh ansible@rpidev`. Do not make configuration changes -- prefer to change the ansible configuration and rerun ansible to make the changes. Use the ansible home folder `/home/ansible/` to store any files 
