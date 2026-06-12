import subprocess
import re
import time
import sys
import os
import threading

def stream_logs(proc, prefix):
    for line in iter(proc.stdout.readline, ""):
        if line:
            sys.stdout.write(f"{prefix} {line}")
            sys.stdout.flush()

def main():
    print("="*60, flush=True)
    print("🚀 CLOUD SIDELOADLY SUPER-ENGINE (TRANSPARENT MODE)", flush=True)
    print("="*60, flush=True)

    # 1. Start VPN
    print("[*] Starting VPN Server (StrongSwan)...", flush=True)
    subprocess.run(["sudo", "ipsec", "restart"], check=True)
    
    # 2. Start Socat Bridges
    print("[*] Starting Network Bridges (5000 -> 500, 4501 -> 4500)...", flush=True)
    subprocess.Popen(["sudo", "socat", "TCP4-LISTEN:5000,fork,reuseaddr", "UDP4:localhost:500"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.Popen(["sudo", "socat", "TCP4-LISTEN:4501,fork,reuseaddr", "UDP4:localhost:4500"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 3. Stream System Logs (for VPN debugging)
    print("[*] Streaming VPN Handshake Logs (look for 'charon' below):", flush=True)
    log_proc = subprocess.Popen(["sudo", "journalctl", "-u", "strongswan", "-f", "-n", "0"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    threading.Thread(target=stream_logs, args=(log_proc, "[VPN-LOG]"), daemon=True).start()

    # 4. Start Tunnel (Pinggy)
    print("[*] Opening Tunnel via Pinggy...", flush=True)
    tunnel_cmd = ["ssh", "-p", "443", "-tt", "-o", "StrictHostKeyChecking=no", "-R0:localhost:5000", "tcp@a.pinggy.io"]
    tunnel_proc = subprocess.Popen(tunnel_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

    url = None
    port = None

    # 5. Wait for URL
    start_time = time.time()
    print("[*] Waiting for Pinggy to assign a URL (max 60s)...", flush=True)
    while time.time() - start_time < 60:
        line = tunnel_proc.stdout.readline()
        if not line: break
        sys.stdout.write(f"[TUNNEL] {line}")
        sys.stdout.flush()
        
        match = re.search(r'([\w\.]+\.pinggy\.link):(\d+)', line)
        if match:
            url = match.group(1)
            port = match.group(2)
            print("\n" + "🌟" * 20, flush=True)
            print(f"🌟 VPN CONNECTION READY", flush=True)
            print(f"🌟 SERVER: {url}", flush=True)
            print(f"🌟 PORT:   {port}", flush=True)
            print("🌟" * 20 + "\n", flush=True)
            print("[*] ACTION REQUIRED: Connect your iPhone VPN now using the settings above.", flush=True)
            break
    
    if not url:
        print("[!] Tunnel failed to initialize. Check if Pinggy is down.", flush=True)
        return

    # 6. Discovery Loop
    print("[*] Scanner active. Watching for iPhone on virtual USB bridge...", flush=True)
    for i in range(120): # 10 minute window
        # Trigger netmuxd scan (sudo)
        subprocess.Popen(["sudo", "netmuxd", "--host", "10.10.10.1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Check for device (discovery.py)
        try:
            res = subprocess.run(["python3", "scripts/discovery.py"], capture_output=True, text=True)
            if "FOUND UDID:" in res.stdout:
                print("\n" + "#" * 40, flush=True)
                print(res.stdout.strip(), flush=True)
                print("#" * 40 + "\n", flush=True)
                print("[***] SUCCESS: UDID CAPTURED! Setup complete.", flush=True)
                return
        except Exception as e:
            print(f"[!] Scanner error: {e}", flush=True)
        
        if i % 6 == 0:
            print(f"[*] Searching... (Minute {i//12 + 1}/10). Keep the VPN toggle 'ON' on your iPhone.", flush=True)
        time.sleep(5)

    print("[!] Timeout: No device connected. Ensure your VPN status is 'Connected'.", flush=True)

if __name__ == "__main__":
    main()
