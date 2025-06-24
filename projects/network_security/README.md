# Network Security Projects

## Overview
This section contains comprehensive network security projects including real-time network monitoring, device management, traffic analysis, and network data processing. These projects demonstrate practical experience in network security operations and threat detection.

## Projects

### 1. Network Monitoring System
**Location**: `network_monitor/`
- **Main Script**: `network_monitor.py` (54KB - comprehensive monitoring system)
- **Description**: Real-time network monitoring and device management system
- **Skills Demonstrated**:
  - Network traffic analysis and monitoring
  - Device discovery and inventory management
  - Real-time security event detection
  - Automated network monitoring scripts
  - Network device configuration and management

### 2. Network Data Analysis
**File**: `network_data_20250615_200356.csv` (161KB)
- **Description**: Real network traffic data analysis and processing
- **Skills Demonstrated**:
  - Large-scale network data processing
  - Network traffic pattern analysis
  - Data visualization and reporting
  - Network security analytics
  - CSV data manipulation and analysis

### 3. Device Management System
**Files**: `devices.json`, `known_devices.json`
- **Description**: Network device inventory and management system
- **Skills Demonstrated**:
  - Device inventory management
  - JSON data structures for network devices
  - Network asset tracking
  - Device configuration management
  - Network topology documentation

### 4. Network Monitoring Automation
**File**: `network_monitor/start_monitor.command`
- **Description**: Automated network monitoring startup and management
- **Skills Demonstrated**:
  - Shell scripting for network automation
  - Automated security monitoring
  - Process management and automation
  - Cross-platform automation scripts

## Key Competencies
- **Network Traffic Analysis**: Real-time monitoring and analysis of network traffic
- **Device Management**: Comprehensive network device inventory and configuration
- **Security Monitoring**: Automated threat detection and alerting systems
- **Data Processing**: Large-scale network data analysis and reporting
- **Automation**: Script-based network security operations

## Network Security Tools & Technologies
- **Python**: Network monitoring and data processing scripts
- **JSON**: Device configuration and inventory management
- **CSV**: Network data storage and analysis
- **Shell Scripting**: Automation and process management
- **Network Protocols**: TCP/IP, HTTP, DNS analysis
- **Device Discovery**: Automated network device identification

## Security Monitoring Capabilities
- **Real-time Monitoring**: Continuous network traffic analysis
- **Device Discovery**: Automated network device identification
- **Traffic Analysis**: Deep packet inspection and pattern recognition
- **Alert System**: Automated security event notification
- **Data Logging**: Comprehensive network activity logging
- **Reporting**: Automated security and network reports

## Network Data Analysis Features
- **Traffic Pattern Recognition**: Identification of normal vs. anomalous traffic
- **Device Communication Mapping**: Understanding network device interactions
- **Security Event Correlation**: Linking related security events
- **Performance Monitoring**: Network performance and bandwidth analysis
- **Compliance Reporting**: Network security compliance documentation

## Implementation Areas
- **Network Infrastructure Security**: Monitoring and protecting network infrastructure
- **Threat Detection**: Real-time identification of security threats
- **Incident Response**: Network-based incident detection and response
- **Compliance Monitoring**: Ensuring network security compliance
- **Performance Optimization**: Network performance monitoring and optimization

## Industry Standards & Best Practices
- **NIST Cybersecurity Framework**: Network security implementation
- **ISO 27001**: Information security management for networks
- **CIS Controls**: Critical security controls for network infrastructure
- **Network Security Monitoring**: Continuous monitoring best practices
- **Incident Response**: Network-based incident handling procedures

## Tools and Methodologies
- **Network Monitoring Tools**: Custom Python-based monitoring solutions
- **Data Analysis Platforms**: Network traffic data processing and analysis
- **Automation Frameworks**: Script-based network security automation
- **Reporting Systems**: Automated network security reporting
- **Device Management**: Network device inventory and configuration tools

# Network Activity Monitor

A Python-based network monitoring tool that captures and displays network activity on your home network. This tool provides a clean user interface to monitor:
- Device connections
- Network traffic
- Connection duration
- Protocol information
- Data transfer sizes

## Prerequisites

- macOS (tested on MacBook Air)
- Python 3.x
- Homebrew
- Suricata
- Required Python packages (installed automatically in virtual environment):
  - scapy
  - pyshark
  - pandas
  - tkinter (usually comes with Python)

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Create and activate the virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Activate the virtual environment if not already activated:
   ```bash
   source venv/bin/activate
   ```

2. Run the network monitor:
   ```bash
   python network_monitor.py
   ```

3. Use the interface:
   - Click "Start Monitoring" to begin capturing network traffic
   - Click "Stop Monitoring" to stop capturing
   - Click "Save Data" to export the captured data to a CSV file

## Features

- Real-time network traffic monitoring
- Clean, user-friendly interface
- Detailed packet information including:
  - Timestamp
  - Source IP
  - Destination IP
  - Protocol
  - Packet length
  - Connection duration
- Data export to CSV format
- Thread-safe packet processing
- Scrollable interface for large amounts of data

## Security Note

This tool requires root/administrator privileges to capture network packets. Run with appropriate permissions:

```bash
sudo python network_monitor.py
```

## Data Storage

Captured data is stored in memory during the session and can be exported to CSV files. The CSV files are named with the format: `network_data_YYYYMMDD_HHMMSS.csv`

## Troubleshooting

If you encounter permission issues:
1. Ensure you're running the script with sudo
2. Check that your user has the necessary permissions to capture network traffic
3. Verify that Suricata is properly installed and configured

For any other issues, check the console output for error messages. 