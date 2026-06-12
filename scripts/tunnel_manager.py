import subprocess
import re
import time
import sys

def start_tunnel():
    print("[*] Starting Tunnel (Pinggy)...")
    cmd = "ssh -p 443 -tt -o StrictHostKeyChecking=no -R0:localhost:5000 tcp@a.pinggy.io"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    while True:
        line = process.stdout.readline()
        if not line: break
        sys.stdout.write(line)
        sys.stdout.flush()
        
        match = re.search(r'([\w\.]+\.pinggy\.link):(\d+)', line)
        if match:
            url = match.group(1)
            port = match.group(2)
            print("\n" + "!"*50)
            print("🚀 VPN SERVER IS READY")
            print(f"SERVER: {url}")
            print(f"PORT:   {port}")
            print("!"*50 + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    start_tunnel()
