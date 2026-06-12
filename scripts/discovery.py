import subprocess
import time
import os

def get_connected_udid():
    try:
        result = subprocess.run(["idevice_id", "-l"], capture_output=True, text=True)
        udids = result.stdout.strip().split('\n')
        return [u for u in udids if u]
    except Exception as e:
        return []

def main():
    print("[*] Scanner active. Waiting for VPN connection...")
    start_time = time.time()
    while time.time() - start_time < 300: # 5 minute window
        devices = get_connected_udid()
        if devices:
            print("\n" + "!"*40)
            print(f"FOUND UDID: {devices[0]}")
            print("!"*40 + "\n")
            return
        time.sleep(2)
    print("[!] Timeout.")

if __name__ == "__main__":
    main()
