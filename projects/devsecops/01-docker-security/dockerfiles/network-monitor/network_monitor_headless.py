#!/usr/bin/env python3
"""
Headless Network Monitor for Container Deployment
This version runs without GUI dependencies for Kubernetes deployment
"""

import threading
import time
from datetime import datetime
import pandas as pd
from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP, Ether, DNS
import pyshark
import queue
import json
import os
from collections import defaultdict
import socket
import re
from mac_vendor_lookup import MacLookup
import hashlib
import csv
import subprocess
import logging
from flask import Flask, jsonify, request
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/network_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Flask app for health checks and API
app = Flask(__name__)

# Global variables
capture_thread = None
stop_capture = False
packet_queue = queue.Queue()
devices = {}
known_devices = {}
device_categories = {}
device_notes = {}
connection_history = []

# Service definitions (same as original)
SERVICES = {
    'streaming': {
        'name': 'Video Streaming',
        'ports': {'tcp': [80, 443, 1935], 'udp': []},
        'domains': ['netflix.com', 'youtube.com', 'hulu.com', 'disneyplus.com']
    },
    'gaming': {
        'name': 'Gaming',
        'ports': {'tcp': [3074, 3075, 3478, 3479, 3480, 7777, 7778, 7779, 3659, 25565], 'udp': [3074, 3075, 3478, 3479, 3480, 7777, 7778, 7779, 3659]},
        'domains': ['playstation.net', 'xboxlive.com', 'steam-chat.com', 'ea.com', 'battle.net']
    },
    'social': {
        'name': 'Social Media',
        'ports': {'tcp': [80, 443], 'udp': []},
        'domains': ['facebook.com', 'twitter.com', 'instagram.com', 'tiktok.com', 'linkedin.com']
    }
}

COMMON_PORT_SERVICES = {
    53: 'DNS', 80: 'HTTP', 443: 'HTTPS', 25: 'SMTP', 110: 'POP3',
    143: 'IMAP', 993: 'IMAPS', 995: 'POP3S', 22: 'SSH', 21: 'FTP'
}

class ServiceDetector:
    @staticmethod
    def extract_ports(info):
        try:
            if 'Port:' in info:
                ports_str = info.split('Port:')[1].strip()
                if '->' in ports_str:
                    src_port, dst_port = ports_str.split('->')
                    return int(src_port.strip()), int(dst_port.strip())
        except:
            pass
        return None, None

    @staticmethod
    def detect_service(packet_info):
        protocol = packet_info['protocol'].lower()
        info = packet_info['info']
        destination = packet_info.get('destination', '')
        src_port, dst_port = ServiceDetector.extract_ports(info)

        # Check for common services
        if dst_port in COMMON_PORT_SERVICES:
            return COMMON_PORT_SERVICES[dst_port]

        # Check for service patterns in domains
        for service_name, service_info in SERVICES.items():
            for domain in service_info['domains']:
                if domain in destination.lower():
                    return service_info['name']

        return 'Unknown'

class DeviceManager:
    def __init__(self):
        self.devices_file = '/app/devices.json'
        self.known_devices_file = '/app/known_devices.json'
        self.load_devices()
        self.load_known_devices()

    def load_devices(self):
        try:
            if os.path.exists(self.devices_file):
                with open(self.devices_file, 'r') as f:
                    self.devices = json.load(f)
        except Exception as e:
            logger.error(f"Error loading devices: {e}")
            self.devices = {}

    def save_devices(self):
        try:
            with open(self.devices_file, 'w') as f:
                json.dump(self.devices, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving devices: {e}")

    def get_manufacturer(self, mac):
        try:
            mac_lookup = MacLookup()
            return mac_lookup.lookup(mac)
        except:
            return "Unknown"

    def update_device(self, mac, ip, info=None):
        if mac not in self.devices:
            self.devices[mac] = {
                'ip': ip,
                'first_seen': datetime.now().isoformat(),
                'last_seen': datetime.now().isoformat(),
                'manufacturer': self.get_manufacturer(mac),
                'device_type': self.detect_device_type(mac, self.get_manufacturer(mac)),
                'connections': [],
                'services': defaultdict(int)
            }
        else:
            self.devices[mac]['last_seen'] = datetime.now().isoformat()
            if ip != self.devices[mac]['ip']:
                self.devices[mac]['ip'] = ip

        if info:
            self.devices[mac]['connections'].append({
                'timestamp': datetime.now().isoformat(),
                'info': info
            })

        self.save_devices()

    def detect_device_type(self, mac_address, manufacturer):
        manufacturer_lower = manufacturer.lower()
        
        if any(keyword in manufacturer_lower for keyword in ['apple', 'iphone', 'ipad', 'macbook']):
            return 'Apple Device'
        elif any(keyword in manufacturer_lower for keyword in ['samsung', 'android']):
            return 'Android Device'
        elif any(keyword in manufacturer_lower for keyword in ['microsoft', 'xbox']):
            return 'Microsoft Device'
        elif any(keyword in manufacturer_lower for keyword in ['sony', 'playstation']):
            return 'Sony Device'
        elif any(keyword in manufacturer_lower for keyword in ['nintendo']):
            return 'Nintendo Device'
        elif any(keyword in manufacturer_lower for keyword in ['router', 'gateway', 'modem']):
            return 'Network Device'
        else:
            return 'Unknown Device'

    def load_known_devices(self):
        try:
            if os.path.exists(self.known_devices_file):
                with open(self.known_devices_file, 'r') as f:
                    self.known_devices = json.load(f)
        except Exception as e:
            logger.error(f"Error loading known devices: {e}")
            self.known_devices = {}

class NetworkMonitor:
    def __init__(self):
        self.device_manager = DeviceManager()
        self.capture_thread = None
        self.stop_capture = False
        self.interface = None
        self.packet_count = 0
        self.start_time = datetime.now()

    def get_available_interfaces(self):
        try:
            result = subprocess.run(['ifconfig'], capture_output=True, text=True)
            interfaces = []
            for line in result.stdout.split('\n'):
                if ':' in line and not line.startswith('\t'):
                    interface = line.split(':')[0]
                    if interface and interface != 'lo':
                        interfaces.append(interface)
            return interfaces
        except Exception as e:
            logger.error(f"Error getting interfaces: {e}")
            return ['eth0', 'en0', 'wlan0']  # Default fallback

    def start_capture(self, interface=None):
        if not interface:
            interfaces = self.get_available_interfaces()
            interface = interfaces[0] if interfaces else 'eth0'
        
        self.interface = interface
        self.stop_capture = False
        self.capture_thread = threading.Thread(target=self.capture_packets)
        self.capture_thread.daemon = True
        self.capture_thread.start()
        logger.info(f"Started packet capture on interface: {interface}")

    def stop_capture(self):
        self.stop_capture = True
        if self.capture_thread:
            self.capture_thread.join()
        logger.info("Stopped packet capture")

    def capture_packets(self):
        try:
            logger.info(f"Starting packet capture on {self.interface}")
            sniff(iface=self.interface, prn=self.process_packet, store=0, stop_filter=lambda x: self.stop_capture)
        except Exception as e:
            logger.error(f"Error in packet capture: {e}")

    def process_packet(self, packet):
        try:
            self.packet_count += 1
            
            if IP in packet:
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                
                # Get MAC addresses
                src_mac = packet[Ether].src if Ether in packet else "Unknown"
                dst_mac = packet[Ether].dst if Ether in packet else "Unknown"
                
                # Update device information
                self.device_manager.update_device(src_mac, src_ip)
                self.device_manager.update_device(dst_mac, dst_ip)
                
                # Log significant packets
                if self.packet_count % 100 == 0:
                    logger.info(f"Processed {self.packet_count} packets")
                    
        except Exception as e:
            logger.error(f"Error processing packet: {e}")

# Flask routes for health checks and API
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'packets_processed': getattr(monitor, 'packet_count', 0),
        'uptime': str(datetime.now() - getattr(monitor, 'start_time', datetime.now()))
    })

@app.route('/ready')
def ready():
    return jsonify({
        'status': 'ready',
        'interface': getattr(monitor, 'interface', 'none'),
        'capture_active': monitor.capture_thread and monitor.capture_thread.is_alive() if hasattr(monitor, 'capture_thread') else False
    })

@app.route('/devices')
def get_devices():
    return jsonify(monitor.device_manager.devices)

@app.route('/stats')
def get_stats():
    return jsonify({
        'packets_processed': monitor.packet_count,
        'devices_found': len(monitor.device_manager.devices),
        'uptime': str(datetime.now() - monitor.start_time),
        'interface': monitor.interface
    })

def main():
    global monitor
    monitor = NetworkMonitor()
    
    # Start packet capture
    monitor.start_capture()
    
    # Start Flask app
    logger.info("Starting Flask app on port 8080")
    app.run(host='0.0.0.0', port=8080, debug=False)

if __name__ == '__main__':
    main() 