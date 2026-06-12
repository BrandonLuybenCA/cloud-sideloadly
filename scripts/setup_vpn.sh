#!/bin/bash
# IKEv2 Setup with PSK (Pre-Shared Key)
sudo apt-get update && sudo apt-get install -y strongswan libcharon-extra-plugins

# Configure VPN with PSK
sudo cat <<VPN_CONF > /etc/ipsec.conf
config setup
    charondebug="ike 1, knl 1, cfg 1"

conn sideloadly
    keyexchange=ikev2
    left=%any
    leftid=@sideloadly-runner
    leftsubnet=10.10.10.0/24
    right=%any
    rightid=@client
    rightsourceip=10.10.10.0/24
    authby=secret
    auto=add
VPN_CONF

# Set the Shared Secret
sudo bash -c 'echo "@sideloadly-runner @client : PSK \"sideloadly123\"" > /etc/ipsec.secrets'

# Start VPN
sudo ipsec restart
echo "[*] VPN Server is Live with PSK: sideloadly123"
