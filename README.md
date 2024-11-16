
# PMKID Collector and Converter Tool

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Description

This tool automates the process of capturing PMKID from Wi-Fi networks and converting the captured `.pcapng` file into the `.hc22000` format, which can then be used with [Hashcat](https://hashcat.net/hashcat/). The script leverages utilities such as `airmon-ng`, `hcxdumptool`, and `hcxpcapngtool` to provide an efficient and streamlined workflow for network penetration testing.

⚠️ **Disclaimer**: This tool is intended for educational purposes and security testing on networks you own or have explicit permission to test. Unauthorized use is illegal and punishable by law.

## Features

- Automated monitor mode activation and deactivation.
- PMKID capture using `hcxdumptool`.
- Conversion of captured `.pcapng` files to `.hc22000` format for Hashcat cracking.
- User-friendly interface with interactive prompts.
- Lightweight and easy to integrate into existing pentesting setups.

## Requirements

Before using this tool, ensure that your system meets the following requirements:

- **Operating System**: Linux (Tested on Kali Linux and Ubuntu)
- **Python Version**: Python 3.6 or higher
- **Dependencies**:
  - `airmon-ng`
  - `hcxdumptool`
  - `hcxpcapngtool`

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/redglobule/PMKIDSniffer.git
cd PMKIDSniffer/
```

### 2. Install Python Dependencies

Although the script itself does not have any Python-specific library dependencies, you should ensure Python 3 is installed:

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

### 3. Install Required Tools

Install the necessary utilities:

```bash
sudo apt update
sudo apt install aircrack-ng hcxdumptool -y
```

For the `hcxpcapngtool` utility, if it is not included with `hcxdumptool`, you can install it as follows:

```bash
sudo apt install hcxtools -y
```

## Usage

### 1. Run the Script

To use the tool, simply execute the script with superuser privileges:

```bash
sudo python3 main.py
```

### 2. Enter the Wi-Fi Interface

The script will prompt you to enter your Wi-Fi interface. Make sure to use the correct interface name (e.g., `wlan0`):

```bash
Enter Interface name: wlan0
```

### 3. PMKID Capture

The script will automatically:
- Kill any conflicting processes.
- Put your Wi-Fi interface in monitor mode.
- Start the PMKID capture using `hcxdumptool`.

You can stop the capture at any time by pressing **Enter**.

### 4. File Conversion

Once the capture is stopped, the script will convert the `.pcapng` file into the `.hc22000` format using `hcxpcapngtool`.

### 5. Output Files

Captured files will be saved in the `captured_pcapng` directory:
- `.pcapng` file: Raw capture file containing PMKID.
- `.hc22000` file: Converted file ready for cracking with Hashcat.

Example of running Hashcat on the converted file:
```bash
hashcat -m 22000 -a 3 yourfile.hc22000 ?a?a?a?a?a?a?a?a
```

## Troubleshooting

### Common Issues

1. **Permission Denied**:
   - Ensure you run the script with `sudo`.
   - Check if your user has the correct permissions to access the Wi-Fi interface.

2. **Dependencies Not Found**:
   - Verify that all tools (`airmon-ng`, `hcxdumptool`, `hcxpcapngtool`) are installed using:
     ```bash
     which airmon-ng
     which hcxdumptool
     which hcxpcapngtool
     ```

3. **Wi-Fi Interface Not in Monitor Mode**:
   - If the interface does not switch to monitor mode, check with:
     ```bash
     iwconfig wlan0
     ```
   - Manually set it to monitor mode:
     ```bash
     sudo airmon-ng start wlan0
     ```

4. **No PMKID Captured**:
   - Make sure you are close to the target Wi-Fi network.
   - Ensure the network supports WPA2-PSK, as PMKID collection is specific to this protocol.

## Contributing

Contributions are welcome! If you would like to improve the script, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Happy hacking! Stay ethical and legal when using this tool.
