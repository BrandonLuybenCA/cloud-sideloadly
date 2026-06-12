import subprocess
import re
import time
import sys
import os
import threading

# Force unbuffered stdout
sys.stdout.reconfigure(line_buffering=True)

def stream_logs(proc, prefix):
    print(f"[*] Started log stream for {prefix}")
    for line in iter(proc.stdout.readline, ""):
        if line:
            print(f"{prefix} {line.strip()}", flush=True)

def main():
    print("!!! ENGINE BOOTING !!!", flush=True)
    try:
        print("="*60, flush=True)
        print("🚀 CLOUD SIDELOADLY SUPER-ENGINE v2 (ULTRA-VOICE)", flush=True)
        print("="*60, flush=True)

        # 1. Start VPN
        print("[*] Step 1: Restarting VPN Server...", flush=True)
        subprocess.run(["sudo", "ipsec", "restart"], check=True)
        
        # 2. Start Socat Bridges
        print("[*] Step 2: Launching Network Bridges...", flush=True)
        subprocess.Popen(["sudo", "socat", "TCP4-LISTEN:5000,fork,reuseaddr", "UDP4:localhost:500"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.Popen(["sudo", "socat", "TCP4-LISTEN:4501,fork,reuseaddr", "UDP4:localhost:4500"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 3. Stream System Logs
        print("[*] Step 3: Opening VPN Log Stream...", flush=True)
        try:
            log_proc = subprocess.Popen(["sudo", "journalctl", "-u", "strongswan", "-f", "-n", "0"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            threading.Thread(target=stream_logs, args=(log_proc, "[VPN]"), daemon=True).start()
        except Exception as log_e:
            print(f"[!] Warning: Could not start VPN log stream: {log_e}", flush=True)

        # 4. Start Tunnel (Pinggy)
        print("[*] Step 4: Connecting to Pinggy Relay...", flush=True)
        tunnel_cmd = ["ssh", "-p", "443", "-tt", "-o", "StrictHostKeyChecking=no", "-R0:localhost:5000", "tcp@a.pinggy.io"]
        tunnel_proc = subprocess.Popen(tunnel_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

        url = None
        port = None

        # 5. Wait for URL
        print("[*] Step 5: Waiting for Public URL...", flush=True)
        start_time = time.time()
        while time.time() - start_time < 60:
            line = tunnel_proc.stdout.readline()
            if not line: break
            print(f"[TUNNEL] {line.strip()}", flush=True)
            
            match = re.search(r'([\w\.]+\.pinggy\.link):(\d+)', line)
            if match:
                url = match.group(1)
                port = match.group(2)
                print("\n" + "🌟" * 15, flush=True)
                print(f"🌟 VPN IS LIVE!", flush=True)
                print(f"🌟 SERVER: {url}", flush=True)
                print(f"🌟 PORT:   {port}", flush=True)
                print("🌟" * 15 + "\n", flush=True)
                print("[!] ACTION: Connect your iPhone VPN now.", flush=True)
                break
        
        if not url:
            print("[!] FATAL: Tunnel timeout. Check Pinggy status.", flush=True)
            return

        # 6. Discovery Loop
        print("[*] Step 6: Scanner Initialized. Watching for iPhone...", flush=True)
        for i in range(120):
            subprocess.Popen(["sudo", "netmuxd", "--host", "10.10.10.1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                res = subprocess.run(["python3", "scripts/discovery.py"], capture_output=True, text=True)
                if "FOUND UDID:" in res.stdout:
                    print("\n" + "✅" * 20, flush=True)
                    print(res.stdout.strip(), flush=True)
                    print("✅" * 20 + "\n", flush=True)
                    return
            except: pass
            
            if i % 6 == 0:
                print(f"[*] Discovery Status: Minute {i//12 + 1}/10. Keep VPN active.", flush=True)
            time.sleep(5)

    except Exception as e:
        print(f"\n[!!!] CRITICAL ENGINE ERROR: {e}", flush=True)

if __name__ == "__main__":
    main()
