#!/bin/bash
sudo apt-get update && sudo apt-get install -y strongswan libcharon-extra-plugins
sudo cat <<VPN_CONF > /etc/ipsec.conf
config setup
    charondebug="ike 2, knl 2, cfg 2"
conn sideloadly
    keyexchange=ikev2
    ike=aes256-sha256-modp2048!
    esp=aes256-sha256!
    left=%any
    leftauth=pubkey
    leftid=@sideloadly-runner
    leftsubnet=10.10.10.0/24
    right=%any
    rightauth=pubkey
    rightid=%any
    rightsourceip=10.10.10.0/24
    auto=add
VPN_CONF
sudo ipsec restart
echo "[*] VPN Server is Live."
