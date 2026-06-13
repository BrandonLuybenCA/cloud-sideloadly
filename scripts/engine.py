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
    
    if os.path.exists("inbox/payload.ipa"):
        print("[*] Ingestion Success: Payload identified in secure inbox.")
    else:
        print("[!] Warning: No payload found in inbox. Running in passive mode.")

    print("[*] Engaging Cloudflare WARP Stealth Shield...")
    subprocess.run(["warp-cli", "--accept-tos", "register"], capture_output=True)
    subprocess.run(["warp-cli", "--accept-tos", "connect"], capture_output=True)
    time.sleep(5)

    print("[*] Starting High-Performance IKEv2 Server...")
    subprocess.run(["sudo", "ipsec", "restart"], check=True)

    print("[*] Establishing Pinggy UDP Relay...")
    tunnel_cmd = ["ssh", "-p", "443", "-tt", "-o", "StrictHostKeyChecking=no", "-R0:localhost:500", "tcp@a.pinggy.io"]
    tunnel_proc = subprocess.Popen(tunnel_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in iter(tunnel_proc.stdout.readline, ""):
        print(f"[TUNNEL] {line.strip()}", flush=True)
        if "pinggy.link" in line:
            print("\n" + "🚀" * 15)
            print("🚀 COMMAND CENTER READY")
            print(f"🚀 {line.strip()}")
            print("🚀" * 15 + "\n")
            break

    print("[*] Sideloading Engine active. Waiting for iPhone VPN connection...")

if __name__ == "__main__":
    main()
