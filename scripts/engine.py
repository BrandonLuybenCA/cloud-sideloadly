import subprocess
import re
import time
import sys
import os
import threading
import argparse

# Force unbuffered stdout
sys.stdout.reconfigure(line_buffering=True)

def stream_logs(proc, prefix):
    for line in iter(proc.stdout.readline, ""):
        if line:
            print(f"{prefix} {line.strip()}", flush=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', default='discovery')
    args = parser.parse_args()

    print("!!! ENGINE BOOTING !!!", flush=True)
    print("="*60, flush=True)
    print(f"🚀 CLOUD SIDELOADLY ENGINE - MODE: {args.mode.upper()}", flush=True)
    print("="*60, flush=True)

    # 1. Start VPN
    print("[*] Starting VPN Server...", flush=True)
    subprocess.run(["sudo", "ipsec", "restart"], check=True)
    
    # 2. Start Tunnel (Pinggy)
    print("[*] Opening Tunnel...", flush=True)
    tunnel_cmd = ["ssh", "-p", "443", "-tt", "-o", "StrictHostKeyChecking=no", "-R0:localhost:500", "tcp@a.pinggy.io"]
    tunnel_proc = subprocess.Popen(tunnel_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

    url = ""
    start_time = time.time()
    while time.time() - start_time < 60:
        line = tunnel_proc.stdout.readline()
        if not line: break
        if "pinggy.link" in line:
            url = line.strip()
            print(f"\n🌟 VPN SERVER READY: {url}\n", flush=True)
            break
    
    # 3. Handle Modes
    if args.mode == 'discovery':
        print("[*] Waiting for iPhone to connect to VPN for UDID capture...", flush=True)
        # Running netmuxd and discovery.py
        subprocess.Popen(["sudo", "netmuxd", "--host", "10.10.10.1"], stdout=subprocess.DEVNULL)
        for i in range(120):
            res = subprocess.run(["python3", "scripts/discovery.py"], capture_output=True, text=True)
            if "FOUND UDID:" in res.stdout:
                print(res.stdout, flush=True)
                return
            time.sleep(5)
    
    elif args.mode == 'sideload':
        print("[*] Sideloading Mode Active. Waiting for VPN connection...", flush=True)
        # Wait for device
        subprocess.Popen(["sudo", "netmuxd", "--host", "10.10.10.1"], stdout=subprocess.DEVNULL)
        
        # Pull environment variables
        ipa_url = os.environ.get('IPA_URL')
        apple_id = os.environ.get('APPLE_ID')
        apple_pass = os.environ.get('APPLE_PASSWORD')
        fake_name = os.environ.get('FAKE_NAME', 'Calculator')
        
        print(f"[*] Downloading IPA: {ipa_url}", flush=True)
        subprocess.run(["curl", "-L", ipa_url, "-o", "app.ipa"], check=True)
        
        print("[*] Signing app with zsign...", flush=True)
        # Note: In a real scenario, we'd use anisette-v3 here to get the cert
        # For this version, we assume zsign/anisette are pre-configured or handled via scripts/sign_and_deploy.py
        subprocess.run(["python3", "scripts/sign_and_deploy.py", "--ipa", "app.ipa", "--name", fake_name], check=True)

if __name__ == "__main__":
    main()
