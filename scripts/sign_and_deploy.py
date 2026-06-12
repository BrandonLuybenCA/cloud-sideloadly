import argparse
import os
import subprocess
import requests
import shutil

def reskin_app(ipa_path, new_name, new_bundle_id):
    print(f"[*] Reskinning: {new_name} ({new_bundle_id})")
    subprocess.run(["unzip", "-q", ipa_path, "-d", "temp_app"])
    payload_dir = os.path.join("temp_app", "Payload")
    app_folder = [os.path.join(payload_dir, d) for d in os.listdir(payload_dir) if d.endswith(".app")][0]
    # Change Name
    plist_path = os.path.join(app_folder, "Info.plist")
    subprocess.run(["plutil", "-replace", "CFBundleDisplayName", "-string", new_name, plist_path])
    subprocess.run(["plutil", "-replace", "CFBundleName", "-string", new_name, plist_path])
    # Change Bundle ID
    subprocess.run(["plutil", "-replace", "CFBundleIdentifier", "-string", new_bundle_id, plist_path])
    # Repackage
    os.remove(ipa_path)
    shutil.make_archive("resigned_app", "zip", "temp_app")
    os.rename("resigned_app.zip", ipa_path)
    shutil.rmtree("temp_app")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ipa", required=True)
    parser.add_argument("--name")
    parser.add_argument("--id")
    args = parser.parse_args()
    if args.name and args.id:
        reskin_app(args.ipa, args.name, args.id)

if __name__ == "__main__":
    main()
