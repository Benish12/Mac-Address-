#!/usr/bin/env python

import subprocess
import optparse
import re
import datetime


# -----------------------------------
# Parse Command Line Arguments
# -----------------------------------

def parser():

    parser = optparse.OptionParser()

    parser.add_option(
        "-i",
        "--interface",
        dest="interface",
        help="Interface to change MAC address"
    )

    parser.add_option(
        "-m",
        "--mac",
        dest="mac",
        help="New MAC address"
    )

    (options, args) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify interface")

    elif not options.mac:
        parser.error("[-] Please specify new MAC address")

    return options
# -----------------------------------
# Validate MAC Address Format
# -----------------------------------

def validate_mac(mac):

    pattern = r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"

    if re.match(pattern, mac):
        return True

    return False

    

    # Check locally administered MAC address
    first_byte = int(mac.split(":")[0], 16)

    if not (first_byte & 2):
        return False

    return True



# -----------------------------------
# Get Current MAC Address
# -----------------------------------

def get_curr_mac(interface):

    try:

        result = subprocess.check_output(
            ["ifconfig", interface]
        ).decode()

        mac_result = re.search(
            r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",
            result
        )

        if mac_result:
            return mac_result.group(0)

        else:
            return None

    except:

        print(
            "[-] Could not read MAC address"
        )

        return None


# -----------------------------------
# Change MAC Address
# -----------------------------------

def mac_changer(interface, new_mac):

    print(
        "[+] Changing MAC address for "
        + interface
        + " to "
        + new_mac
    )

    subprocess.call(
        "ifconfig " + interface + " down",
        shell=True
    )

    subprocess.call(
        "ifconfig " + interface +
        " hw ether " + new_mac,
        shell=True
    )

    subprocess.call(
        "ifconfig " + interface + " up",
        shell=True
    )


# -----------------------------------
# Create Security Log
# -----------------------------------

def create_log(interface, old_mac, new_mac, status):

    with open(
        "mac_change.log",
        "a"
    ) as file:

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
# Main Program
# -----------------------------------

options = parser()


old_mac = get_curr_mac(
    options.interface
)


print(
    "[+] Old MAC address: "
    + str(old_mac)
)


if validate_mac(options.mac):

    mac_changer(
        options.interface,
        options.mac
    )

    current_mac = get_curr_mac(
        options.interface
    )


    if current_mac.lower() == options.mac.lower():

        print(
            "[+] MAC address changed successfully"
        )

        print(
            "[+] New MAC address: "
            + current_mac
        )


        create_log(
            options.interface,
            old_mac,
            current_mac,
            "SUCCESS"
        )


    else:

        print(
            "[-] MAC address change failed"
        )


        create_log(
            options.interface,
            old_mac,
            options.mac,
            "FAILED"
        )


else:

    print(
        "[-] Invalid MAC address format"
    )

    print(
        "[!] Correct format example: 00:11:22:33:44:55"
    )
