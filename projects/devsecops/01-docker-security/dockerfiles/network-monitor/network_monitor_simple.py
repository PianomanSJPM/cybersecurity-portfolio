#!/usr/bin/env python3
"""
Simple Network Monitor for Container Deployment
This version runs without complex dependencies for Kubernetes deployment
"""

import threading
import time
from datetime import datetime
import json
import os
import socket
import subprocess
import logging
from flask import Flask, jsonify
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
monitor = None

class SimpleNetworkMonitor:
    def __init__(self):
        self.capture_thread = None
        self.stop_capture = False
        self.interface = None
        self.packet_count = 0
        self.start_time = datetime.now()
        self.devices = {}
        self.devices_file = '/app/devices.json'
        self.load_devices()

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
            # Use tcpdump for packet capture
            cmd = ['tcpdump', '-i', self.interface, '-n', '-l']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            for line in process.stdout:
                if self.stop_capture:
                    break
                self.process_packet_line(line)
                
        except Exception as e:
            logger.error(f"Error in packet capture: {e}")

    def process_packet_line(self, line):
        try:
            self.packet_count += 1
            
            # Simple packet parsing
            if 'IP' in line:
                # Extract IP addresses
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == 'IP' and i + 1 < len(parts):
                        src_dst = parts[i + 1]
                        if '>' in src_dst:
                            src, dst = src_dst.split('>')
                            self.update_device_info(src.strip(), dst.strip())
                            break
            
            # Log significant packets
            if self.packet_count % 100 == 0:
                logger.info(f"Processed {self.packet_count} packets")
                    
        except Exception as e:
            logger.error(f"Error processing packet line: {e}")

    def update_device_info(self, src, dst):
        try:
            # Extract IP addresses
            src_ip = src.split(':')[0] if ':' in src else src
            dst_ip = dst.split(':')[0] if ':' in dst else dst
            
            # Update device information
            if src_ip not in self.devices:
                self.devices[src_ip] = {
                    'ip': src_ip,
                    'first_seen': datetime.now().isoformat(),
                    'last_seen': datetime.now().isoformat(),
                    'connections': []
                }
            else:
                self.devices[src_ip]['last_seen'] = datetime.now().isoformat()
            
            if dst_ip not in self.devices:
                self.devices[dst_ip] = {
                    'ip': dst_ip,
                    'first_seen': datetime.now().isoformat(),
                    'last_seen': datetime.now().isoformat(),
                    'connections': []
                }
            else:
                self.devices[dst_ip]['last_seen'] = datetime.now().isoformat()
            
            # Add connection
            connection = {
                'timestamp': datetime.now().isoformat(),
                'src': src_ip,
                'dst': dst_ip
            }
            
            self.devices[src_ip]['connections'].append(connection)
            self.devices[dst_ip]['connections'].append(connection)
            
            # Save periodically
            if self.packet_count % 50 == 0:
                self.save_devices()
                
        except Exception as e:
            logger.error(f"Error updating device info: {e}")

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
    return jsonify(monitor.devices)

@app.route('/stats')
def get_stats():
    return jsonify({
        'packets_processed': monitor.packet_count,
        'devices_found': len(monitor.devices),
        'uptime': str(datetime.now() - monitor.start_time),
        'interface': monitor.interface
    })

def main():
    global monitor
    monitor = SimpleNetworkMonitor()
    
    # Start packet capture
    monitor.start_capture()
    
    # Start Flask app
    logger.info("Starting Flask app on port 8080")
    app.run(host='0.0.0.0', port=8080, debug=False)

if __name__ == '__main__':
    main() 