#!/bin/bash
set -e
echo "[*] Installing StrongSwan for Ubuntu 24.04..."
sudo apt-get update -y
sudo apt-get install -y strongswan strongswan-pki libcharon-extra-plugins libcharon-extauth-plugins socat
sudo ipsec restart
sleep 5
