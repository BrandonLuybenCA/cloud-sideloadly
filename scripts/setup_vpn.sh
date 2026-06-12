#!/bin/bash
set -e
echo "[*] Installing StrongSwan and Socat..."
sudo apt-get update -y
sudo apt-get install -y strongswan libcharon-extra-plugins libcharon-standard-plugins socat

echo "[*] Configuring StrongSwan (IKEv2 over TCP)..."
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
    # Enable IKEv2 over TCP (RFC 8229)
    # Most clients use port 4500 for this, but we bridge to 500/4500
    ike=aes256-sha256-modp2048!
    esp=aes256-sha256!
VPN_CONF

sudo cat <<VPN_SEC > /etc/ipsec.secrets
: PSK "sideloadly123"
VPN_SEC

echo "[*] Starting StrongSwan..."
# Use ipsec command directly instead of systemctl as it's more reliable in GHA containers
sudo ipsec restart
sleep 5
sudo ipsec statusall || true
