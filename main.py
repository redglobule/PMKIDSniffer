import subprocess
import threading
import os
import sys
from datetime import datetime

# User input for Wi-Fi interface
interface = str(input("Enter Interface name: "))

# Event to stop capture
stop_capture = threading.Event()

# Function to check if the script is run as sudo
def check_permissions():
    if os.geteuid() != 0:
        print("\033[0;31m[ERROR] The script must be run as a superuser (sudo)\033[0m")
        sys.exit(1)

# Function to check if required tools are installed
def check_dependencies():
    tools = ["airmon-ng", "hcxdumptool", "hcxpcapngtool"]
    for tool in tools:
        if subprocess.call(f"which {tool}", shell=True, stdout=subprocess.DEVNULL) != 0:
            print(f"\033[0;31m[ERROR] {tool} is not installed. Please install it.\033[0m")
            sys.exit(1)

# Function to activate monitor mode on Wi-Fi interface
def activate_wifi_monitor(interface):
    commands = [
        (["sudo", "airmon-ng", "check", "kill"], "Killing conflicting processes"),
        (["sudo", "airmon-ng", "start", interface], "Starting monitor mode")
    ]
    
    for cmd, msg in commands:
        try:
            print(f"\033[0;33m{msg}...\033[0m")
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"\033[0;32m- {msg} successful\033[0m\n")
        except subprocess.CalledProcessError as e:
            print(f"\033[0;31m[ERROR] {msg} failed: {e.stderr.strip()}\033[0m")
            return False

    # Verify if the interface is in monitor mode
    result = subprocess.run(["iwconfig", interface], capture_output=True, text=True)
    if "Mode:Monitor" in result.stdout:
        print(f"\033[0;32m- {interface} is in Monitor mode\033[0m\n")
        return True
    else:
        print(f"\033[0;31m[ERROR] {interface} is not in Monitor mode\033[0m")
        return False

# Function to collect PMKIDs
def collect_pmkid(interface):
    print("\033[0;33mStarting PMKID capture...\033[0m")
    os.makedirs("captured_pcapng", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pcapng_file = f"captured_pcapng/pmkid_capture_{timestamp}.pcapng"

    process = subprocess.Popen(
        ["sudo", "hcxdumptool", "-i", interface, "-w", pcapng_file, "--disable_deauthentication", "--disable_association"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stopper_thread = threading.Thread(target=stop_on_keypress)
    stopper_thread.start()

    try:
        stop_capture.wait()
        print("\nStopping capture...")
        process.terminate()
    except KeyboardInterrupt:
        process.terminate()

    print(f"\033[0;32mCapture completed. File saved at: {pcapng_file}\033[0m")
    return pcapng_file

# Function to handle user input for stopping the capture
def stop_on_keypress():
    input("Press 'Enter' to stop the capture: ")
    stop_capture.set()

# Function to convert .pcapng file to .hc22000
def convert_to_hc22000(pcapng_file):
    print("\033[0;33mConverting .pcapng to .hc22000...\033[0m")
    output_file = pcapng_file.replace(".pcapng", ".hc22000")
    command = ["hcxpcapngtool", "-o", output_file, pcapng_file]
    
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"\033[0;32mConversion successful! File: {output_file}\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[0;31m[ERROR] Conversion failed: {e.stderr.strip()}\033[0m")

# Function to cleanup and stop monitor mode
def cleanup(interface):
    commands = [
        (["sudo", "airmon-ng", "stop", interface], "Stopping monitor mode"),
        (["sudo", "systemctl", "restart", "NetworkManager"], "Restarting NetworkManager")
    ]

    for cmd, msg in commands:
        try:
            print(f"\033[0;33m{msg}...\033[0m")
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"\033[0;32m- {msg} successful\033[0m\n")
        except subprocess.CalledProcessError as e:
            print(f"\033[0;31m[ERROR] {msg} failed: {e.stderr.strip()}\033[0m")

# Main function
if __name__ == "__main__":
    check_permissions()
    check_dependencies()

    if activate_wifi_monitor(interface):
        pcapng_file = collect_pmkid(interface)
        convert_to_hc22000(pcapng_file)
        cleanup(interface)

