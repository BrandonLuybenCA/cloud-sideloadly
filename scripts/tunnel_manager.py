import subprocess
import re
import time
import sys

def start_tunnel():
    print("[*] Starting Tunnel (Pinggy) on Port 5000...")
    # Map Pinggy TCP port to Runner's TCP port 5000
    cmd = "ssh -p 443 -tt -o StrictHostKeyChecking=no -R0:localhost:5000 tcp@a.pinggy.io"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    start_time = time.time()
    while time.time() - start_time < 60:
        line = process.stdout.readline()
        if not line: break
        print(line.strip())
        
        match = re.search(r'([\w\.]+\.pinggy\.link):(\d+)', line)
        if match:
            url = match.group(1)
            port = match.group(2)
            print("\n" + "!"*50)
            print("🚀 VPN SERVER IS READY")
            print(f"SERVER: {url}")
            print(f"PORT:   {port}")
            print("!"*50 + "\n")
            return True
    return False

if __name__ == "__main__":
    if start_tunnel():
        while True: time.sleep(100)
