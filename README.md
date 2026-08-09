# MAC Address Management & Audit Tool

## Overview

This project is a Python-based Linux tool for managing and auditing MAC addresses on network interfaces.

The tool can detect the current MAC address, validate a new MAC address, back up the original address, change the MAC address, verify the change, restore the original address, and record the activity in an audit log.

I built this project to practice Python, Linux networking, command-line tools, and basic security auditing.

## Features

* Detect the current MAC address
* Validate MAC address format
* Back up the original MAC address
* Change the MAC address
* Verify the MAC address after the change
* Restore the original MAC address
* Create an audit log of MAC address changes
* Use command-line arguments for different operations

## Technologies Used

* Python 3
* Linux
* Bash
* Linux `ip` networking utility
* Regular Expressions
* JSON


## Python Modules

The project uses Python's standard library:

* `subprocess`
* `argparse`
* `re`
* `datetime`
* `json`
* `os`

No external Python packages are required.

## Project Structure

```text
MAC address changer/
│
├── mac_changer.py
├── README.md
└── .gitignore
```

The following files are generated when the program runs and are excluded from GitHub:

```text
mac_backup.json
mac_change.log
__pycache__/
```

## How It Works

The program follows this process:

```text
Identify Interface
       ↓
Read Current MAC
       ↓
Validate New MAC
       ↓
Back Up Original MAC
       ↓
Change MAC Address
       ↓
Verify Change
       ↓
Write Audit Log
```

The restore option uses the backup file to return the interface to its original MAC address.

## Requirements

* Linux
* Python 3
* Network interface
* `sudo` privileges

Check that Python is installed:

```bash
python3 --version
```

Check the Linux networking utility:

```bash
ip --version
```
# Usage

## 1. Find the Network Interface

Run:

```bash
ip link
```

Example:

```text
2: eth0:
```

In this example, the interface is `eth0`.

Your interface may have a different name, such as `enp0s3` or `wlan0`.

## 2. Check the Current MAC Address

Run:

```bash
ip link show eth0
```

Replace `eth0` with your actual interface.

The MAC address appears after:

```text
link/ether

## 3. Check the Python File

Before running the program, check for Python syntax or indentation errors:

```bash
python3 -m py_compile mac_changer.py
```

If there is no output, the file passed the syntax check.

## 4. View the Help Menu

Run:

```bash
python3 mac_changer.py --help
```

Available options:

```text
-i, --interface    Network interface
-m, --mac          New MAC address
--restore          Restore original MAC address

## 5. Change the MAC Address

Run:

```bash
sudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55
```

Replace `eth0` with your network interface.

The program first detects and backs up the current MAC address before attempting the change.

Example output:

```text
[+] Current MAC: XX:XX:XX:XX:XX:XX
[+] Original MAC address backed up
[+] Changing eth0 MAC address to 00:11:22:33:44:55
[+] MAC address changed successfully
```
## 6. Verify the Change

After the program reports a successful change, verify it manually:

```bash
ip link show eth0
```

The output should show the new MAC address.

## 7. Check the Backup

The program creates a backup file named:

```text
mac_backup.json
```

View it with:

```bash
cat mac_backup.json
```

The file contains the original interface and MAC address information needed for restoration.
## 8. Check the Audit Log

The program creates:

```text
mac_change.log
```

View the log with:

```bash
cat mac_change.log
```

The log records:

* Time of the operation
* Network interface
* Original MAC address
* New MAC address
* Operation status

Example:

```text
----------------------------
Time: 2026-08-09 18:00:00
Interface: eth0
Old MAC: XX:XX:XX:XX:XX:XX
New MAC: XX:XX:XX:XX:XX:XX
Status: SUCCESS
```

---

## 9. Restore the Original MAC Address

To restore the original MAC address saved in the backup file:

```bash
sudo python3 mac_changer.py --restore
```

The program reads the original MAC address from `mac_backup.json` and restores it.

## 10. Verify the Restoration

Run:

```bash
ip link show eth0
```

The original MAC address should be displayed again.

# Testing & Results

The tool was tested through the complete MAC address management workflow.

| Test                     | Result |
| ------------------------ | ------ |
| Python syntax validation | Passed |
| MAC address detection    | Passed |
| MAC address validation   | Passed |
| Original MAC backup      | Passed |
| MAC address modification | Passed |
| MAC change verification  | Passed |
| Security audit logging   | Passed |
| MAC address restoration  | Passed |
| Restoration verification | Passed |

The complete workflow was successfully tested from **backup → change → verification → logging → restoration**.

# Challenges and Technical Learning

During development, I worked through several issues involving:

* Python indentation and syntax
* Linux file and directory management
* Identifying network interfaces
* Linux administrative permissions
* Using the `ip` networking utility
* Verifying MAC address changes
* WSL networking limitations
* Creating and using JSON backups
* Implementing audit logging

These challenges provided hands-on experience with Linux networking and Python-based system administration.

# Security Considerations

MAC address changes can affect network connectivity and network access controls.

This tool is intended for:

* Cybersecurity labs
* Personal systems
* Controlled virtual machines
* Authorized security testing
* Linux networking practice

Only use the tool on systems and networks where you have permission to make network configuration changes.

# Future Improvements

Possible future improvements include:

* Add a `--show` option
* Add automatic privilege checking
* Improve error handling
* Support multiple network interfaces
* Add unit tests
* Add structured JSON audit reports
* Add a dry-run option
* Improve rollback and recovery handling

# Skills Demonstrated

**Python • Linux • Bash • Networking • MAC Addresses • Regular Expressions • JSON • File I/O • Subprocess Management • CLI Development • Security Auditing • System Administration

