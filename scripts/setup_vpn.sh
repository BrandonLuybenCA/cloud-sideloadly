#!/bin/bash
set -e
echo "[*] Installing StrongSwan and Socat..."
sudo apt-get update -y
sudo apt-get install -y strongswan libcharon-extra-plugins socat

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

echo "[*] Starting StrongSwan service..."
sudo systemctl restart strongswan-starter
sleep 3
sudo ipsec statusall || true
