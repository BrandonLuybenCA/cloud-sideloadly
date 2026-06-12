#!/bin/bash
set -e
echo "[*] Installing StrongSwan for Ubuntu 24.04..."
sudo apt-get update -y
sudo apt-get install -y strongswan strongswan-pki libcharon-extra-plugins libcharon-extauth-plugins socat

sudo cat <<VPN_CONF > /etc/ipsec.conf
config setup
    charondebug="ike 1, knl 1, cfg 1"

conn sideloadly
    keyexchange=ikev2
    authby=psk
    left=%any
    leftid=@sideloadly-runner
    leftsubnet=0.0.0.0/0
    right=%any
    rightid=@client
    rightsourceip=10.10.10.0/24
    auto=add
    ike=aes256-sha256-modp2048!
    esp=aes256-sha256!
    forceencaps=yes
VPN_CONF

sudo cat <<VPN_SEC > /etc/ipsec.secrets
: PSK "sideloadly123"
VPN_SEC

echo "[*] Restarting StrongSwan..."
sudo ipsec restart
sleep 2
