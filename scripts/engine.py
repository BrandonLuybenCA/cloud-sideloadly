import subprocess
import os
import sys
import time

sys.stdout.reconfigure(line_buffering=True)

def main():
    print("="*60)
    print("🌟 CLOUD SIDELOADLY ULTRA-ENGINE | SHIELD ACTIVE")
    print("="*60)
    print("!!! ENGINE BOOTING !!!")
    
    # 1. Stealth Mask (Cloudflare WARP)
    print("[*] Engaging Cloudflare WARP Stealth Shield...")
    try:
        # Start warp-svc in background using sudo
        subprocess.Popen(["sudo", "warp-svc"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        subprocess.run(["warp-cli", "--accept-tos", "register"], capture_output=True)
        subprocess.run(["warp-cli", "--accept-tos", "connect"], capture_output=True)
        print("[*] Stealth Shield Connected.")
    except Exception as e:
        print(f"[!] Stealth Shield failed: {e}")

    # 2. VPN Startup
    print("[*] Starting High-Performance IKEv2 Server...")
    subprocess.run(["sudo", "ipsec", "restart"], check=True)

    # 3. Tunneling
    print("[*] Establishing Pinggy UDP Relay...")
    tunnel_cmd = ["ssh", "-p", "443", "-tt", "-o", "StrictHostKeyChecking=no", "-R0:localhost:500", "tcp@a.pinggy.io"]
    tunnel_proc = subprocess.Popen(tunnel_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in iter(tunnel_proc.stdout.readline, ""):
        if "pinggy.link" in line:
            print("\n" + "🚀" * 15)
            print("🚀 COMMAND CENTER READY")
            print(f"🚀 {line.strip()}")
            print("🚀" * 15 + "\n")
            break

    print("[*] Engine active. Waiting for iPhone VPN connection...")

if __name__ == "__main__":
    main()
