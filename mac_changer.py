#!/usr/bin/env python3

import argparse
import datetime
import json
import os
import re
import subprocess


# -----------------------------------
# Parse Command Line Arguments
# -----------------------------------

def get_args():

    parser = argparse.ArgumentParser(
        description="MAC Address Management & Audit Tool"
    )

    parser.add_argument(
        "-i",
        "--interface",
        required=False,
        help="Network interface"
    )

    parser.add_argument(
        "-m",
        "--mac",
        required=False,
        help="New MAC address"
    )

    parser.add_argument(
        "--restore",
        action="store_true",
        help="Restore original MAC address"
    )

    return parser.parse_args()


# -----------------------------------
# Validate MAC Address
# -----------------------------------

def validate_mac(mac):

    pattern = r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"

    if not re.match(pattern, mac):
        return False

    # Require a locally administered MAC address.
    first_byte = int(mac.split(":")[0], 16)

    if not (first_byte & 2):
        return False

    return True


# -----------------------------------
# Get Current MAC Address
# -----------------------------------

def get_current_mac(interface):

    try:

        result = subprocess.check_output(
            ["ip", "link", "show", interface],
            stderr=subprocess.STDOUT
        ).decode()

        mac = re.search(
            r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}",
            result
        )

        if mac:
            return mac.group(0)

        return None

    except subprocess.CalledProcessError:

        print("[-] Could not read MAC address")
        return None


# -----------------------------------
# Backup MAC Address
# -----------------------------------

def backup_mac(interface, mac):

    data = {
        "interface": interface,
        "original_mac": mac,
        "backup_time": str(datetime.datetime.now())
    }

    with open("mac_backup.json", "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )

    print("[+] Original MAC address backed up")


# -----------------------------------
# Change MAC Address
# -----------------------------------

def change_mac(interface, new_mac):

    print(
        f"[+] Changing MAC address for {interface} to {new_mac}"
    )

    try:

        subprocess.run(
            ["ip", "link", "set", interface, "down"],
            check=True
        )

        subprocess.run(
            [
                "ip",
                "link",
                "set",
                "dev",
                interface,
                "address",
                new_mac
            ],
            check=True
        )

        subprocess.run(
            ["ip", "link", "set", interface, "up"],
            check=True
        )

        return True

    except subprocess.CalledProcessError:

        print("[-] MAC address change failed")
        return False


# -----------------------------------
# Create Security Log
# -----------------------------------

def create_log(interface, old_mac, new_mac, status):

    with open("mac_change.log", "a") as file:

        file.write(
            "\n----------------------------\n"
        )

        file.write(
            "Time: "
            + str(datetime.datetime.now())
            + "\n"
        )

        file.write(
            "Interface: "
            + interface
            + "\n"
        )

        file.write(
            "Old MAC: "
            + str(old_mac)
            + "\n"
        )

        file.write(
            "New MAC: "
            + str(new_mac)
            + "\n"
        )

        file.write(
            "Status: "
            + status
            + "\n"
        )


# -----------------------------------
# Restore Original MAC Address
# -----------------------------------

def restore_mac():

    if not os.path.exists("mac_backup.json"):

        print("[-] No backup file found")
        return

    with open("mac_backup.json", "r") as file:

        data = json.load(file)

    interface = data["interface"]
    original_mac = data["original_mac"]

    print(
        f"[+] Restoring {interface} to {original_mac}"
    )

    success = change_mac(
        interface,
        original_mac
    )

    if success:

        create_log(
            interface,
            "RESTORE",
            original_mac,
            "SUCCESS"
        )

        print("[+] MAC address restored successfully")

    else:

        create_log(
            interface,
            "RESTORE",
            original_mac,
            "FAILED"
        )


# -----------------------------------
# Main Program
# -----------------------------------

def main():

    options = get_args()

    # Restore mode
    if options.restore:

        restore_mac()
        return

    # Check interface
    if not options.interface:

        print("[-] Please specify interface")
        print(
            "Example: sudo python3 mac_changer.py "
            "-i enp0s3 -m 02:11:22:33:44:55"
        )
        return

    # Check MAC
    if not options.mac:

        print("[-] Please specify new MAC address")
        print(
            "Example: sudo python3 mac_changer.py "
            "-i enp0s3 -m 02:11:22:33:44:55"
        )
        return

    # Validate MAC
    if not validate_mac(options.mac):

        print("[-] Invalid MAC address format")
        print(
            "[!] Use a locally administered MAC address."
        )
        print(
            "[!] Example: 02:11:22:33:44:55"
        )
        return

    # Get current MAC
    old_mac = get_current_mac(
        options.interface
    )

    if not old_mac:

        print("[-] Could not determine current MAC address")
        return

    print(
        "[+] Current MAC:",
        old_mac
    )

    # Backup current MAC
    backup_mac(
        options.interface,
        old_mac
    )

    # Change MAC
    success = change_mac(
        options.interface,
        options.mac
    )

    if not success:

        create_log(
            options.interface,
            old_mac,
            options.mac,
            "FAILED"
        )

        return

    # Verify change
    current_mac = get_current_mac(
        options.interface
    )

    if current_mac and current_mac.lower() == options.mac.lower():

        print(
            "[+] MAC address changed successfully"
        )

        print(
            "[+] New MAC address:",
            current_mac
        )

        create_log(
            options.interface,
            old_mac,
            current_mac,
            "SUCCESS"
        )

    else:

        print(
            "[-] MAC address change could not be verified"
        )

        create_log(
            options.interface,
            old_mac,
            options.mac,
            "FAILED"
        )


# -----------------------------------
# Start Program
# -----------------------------------

if __name__ == "__main__":
    main()