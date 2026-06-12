#!/bin/bash
set -e
echo "[*] Installing StrongSwan..."
sudo apt-get update -y
# In Ubuntu 24.04, we use strongswan and its core plugins
sudo apt-get install -y strongswan strongswan-pki libcharon-extra-plugins libcharon-extauth-plugins socat

echo "[*] Configuring StrongSwan..."
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
    rightaddresspool=10.10.10.0/24
    auto=add
    ike=aes256-sha256-modp2048!
    esp=aes256-sha256!
VPN_CONF

sudo cat <<VPN_SEC > /etc/ipsec.secrets
: PSK "sideloadly123"
VPN_SEC

echo "[*] Starting StrongSwan..."
# Use ipsec restart as it works across init systems in GHA
sudo ipsec restart
sleep 5
sudo ipsec statusall || true
