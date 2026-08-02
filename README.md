# Network Interface MAC Address Security Tool

## Project Overview

This project is a Python-based cybersecurity tool that automates MAC address modification for a network interface. The tool retrieves the current MAC address, validates the new MAC address format, applies the change, verifies the updated configuration, and creates an audit log for tracking security-related changes.

This project was developed in a controlled Linux environment for educational and cybersecurity training purposes.

---

## Features

- Retrieve current MAC address from a network interface
- Change MAC address using Linux networking commands
- Validate MAC address format using Regular Expressions (Regex)
- Verify successful MAC address modification
- Generate timestamped security audit logs
- Provide command-line interface options
- Handle invalid MAC address input

---

## Technologies Used

- Python 3
- Linux Networking Commands
- Bash Terminal
- Regular Expressions (Regex)
- Subprocess Module
- Optparse Module

---

## Python Modules

### subprocess
Used to execute Linux networking commands from Python and interact with the operating system.

### optparse
Used to create command-line arguments for selecting network interfaces and MAC addresses.

### re (Regular Expression)
Used to validate MAC address formats and extract MAC addresses from system output.

### datetime
Used to generate timestamps for security audit logs.

---

## Project Structure
