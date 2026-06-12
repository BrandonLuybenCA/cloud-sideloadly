import subprocess
import re
import time
import os
import sys

def start_pinggy():
    print("[*] Attempting to start Pinggy tunnel...")
    # Use -tt to force a pseudo-terminal so Pinggy outputs the link
    cmd = ['ssh', '-tt', '-o', 'StrictHostKeyChecking=no', '-R', '0:localhost:5000', 'tcp@a.pinggy.io']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    start_time = time.time()
    while time.time() - start_time < 45:
        line = process.stdout.readline()
        if not line:
            break
        print(f"PINGGY: {line.strip()}")
        # Pattern for Pinggy TCP URLs
        match = re.search(r'([a-z0-9]+\.a\.pinggy\.link:\d+)', line)
        if match:
            return match.group(1)
    return None

def start_localhost_run():
    print("[*] Attempting fallback to localhost.run...")
    # Localhost.run is very simple and consistent
    cmd = ['ssh', '-o', 'StrictHostKeyChecking=no', '-R', '80:localhost:5000', 'nokey@localhost.run']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    start_time = time.time()
    while time.time() - start_time < 30:
        line = process.stdout.readline()
        if not line:
            break
        print(f"LHR: {line.strip()}")
        match = re.search(r'([a-z0-9.-]+\.lhr\.life)', line)
        if match:
            # localhost.run on port 80
            return f"{match.group(1)}:80"
    return None

url = start_pinggy()
if not url:
    url = start_localhost_run()

if url:
    print(f"\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(f"🚀 SUCCESS! VPN SERVER IS READY")
    print(f"SERVER: {url.split(':')[0]}")
    print(f"PORT: {url.split(':')[1]}")
    print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
    # Save to GHA environment
    with open(os.environ['GITHUB_ENV'], 'a') as f:
        f.write(f"VPN_URL={url}\n")
else:
    print("[!!!] FAILED TO START ANY TUNNEL")
    sys.exit(1)
