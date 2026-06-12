import subprocess
import re
import time
import sys
import os

def run_cmd_bg(cmd):
    print(f"[*] Starting background process: {cmd}")
    return subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    print("="*50)
    print("🚀 STARTING CLOUD SIDELOADLY ENGINE")
    print("="*50)

    # 1. Start VPN (sudo)
    print("[*] Starting VPN Server...")
    subprocess.run(["sudo", "ipsec", "restart"], check=True)
    
    # 2. Start Socat Bridges (sudo)
    run_cmd_bg("sudo socat TCP4-LISTEN:5000,fork,reuseaddr UDP4:localhost:500")
    run_cmd_bg("sudo socat TCP4-LISTEN:4501,fork,reuseaddr UDP4:localhost:4500")

    # 3. Start Tunnel (Pinggy)
    print("[*] Opening Tunnel...")
    tunnel_cmd = ["ssh", "-p", "443", "-tt", "-o", "StrictHostKeyChecking=no", "-R0:localhost:5000", "tcp@a.pinggy.io"]
    tunnel_proc = subprocess.Popen(tunnel_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

    url = None
    port = None

    # 4. Wait for URL
    start_time = time.time()
    while time.time() - start_time < 60:
        line = tunnel_proc.stdout.readline()
        if not line: break
        sys.stdout.write(line)
        sys.stdout.flush()
        
        match = re.search(r'([\w\.]+\.pinggy\.link):(\d+)', line)
        if match:
            url = match.group(1)
            port = match.group(2)
            print("\n" + "!"*50)
            print("🌟 VPN CONNECTION READY")
            print(f"   SERVER: {url}")
            print(f"   PORT:   {port}")
            print("!"*50 + "\n")
            print("[*] Please connect your iPhone VPN now.")
            break
    
    if not url:
        print("[!] Tunnel failed to initialize.")
        return

    # 5. Discovery Loop
    print("[*] Scanner active. Watching for iPhone...")
    for i in range(100):
        # Trigger netmuxd scan (sudo)
        subprocess.Popen(["sudo", "netmuxd", "--host", "10.10.10.1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Check for device (discovery.py)
        try:
            res = subprocess.run(["python3", "scripts/discovery.py"], capture_output=True, text=True)
            if "UDID:" in res.stdout:
                print(res.stdout)
                print("[***] SUCCESS: UDID CAPTURED!")
                return
        except:
            pass
        
        time.sleep(5)
        if i % 5 == 0:
            print(f"[*] Still searching... (Attempt {i}/100)")

    print("[!] Timeout: No device connected.")

if __name__ == "__main__":
    main()
