#!/usr/bin/env python3

# 

import socket
import os
import time
from datetime import datetime

class VKMaxCore:
    def __init__(self, port=12345):
        self.port = port
        self.nickname = os.getlogin() or 'User'
        self.running = True
        self.socket_timeout = 3
        
    def create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(self.socket_timeout)
        return sock
    
    def start_server(self, host=''):
        server_socket = self.create_socket()
        server_socket.bind((host, self.port))
        server_socket.listen(5)
        
        print(f"VKMax Server listens to port {self.port}")
        
        try:
            while self.running:
                try:
                    conn, addr = server_socket.accept()
                    self.handle_connection(conn, addr)
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\nЫtop listening.")
        finally:
            server_socket.close()
    
    def handle_connection(self, conn, addr):
        try:
            data = conn.recv(4096).decode('utf-8', errors='ignore')
            if data:
                print(f"\n{data}", end='', flush=True)
                print("> ", end='', flush=True)
        except:
            pass
        finally:
            conn.close()
    
    def send_text(self, target_ip, text):
        try:
            sock = self.create_socket()
            sock.connect((target_ip, self.port))
            
            timestamp = datetime.now().strftime("%H:%M")
            message = f"[{timestamp}] {self.nickname}: {text}\n"
            sock.send(message.encode())
            return True, "Message sended"
            
        except ConnectionRefusedError:
            return False, "Server error!"
        except Exception as e:
            return False, f"Send error: {e}"
        finally:
            sock.close()
    
    def send_file(self, target_ip, filepath):
        if not os.path.isfile(filepath):
            return False, "File not found"
        
        try:
            sock = self.create_socket()
            sock.connect((target_ip, self.port))
            
            timestamp = datetime.now().strftime("%H:%M")
            filename = os.path.basename(filepath)
            header = f"[{timestamp}] {self.nickname} sended file: {filename}\n"
            sock.send(header.encode())
            time.sleep(0.1)
            
            with open(filepath, 'rb') as f:
                while chunk := f.read(4096):
                    sock.send(chunk)
            
            return True, "File sended"
            
        except ConnectionRefusedError:
            return False, "Server error"
        except Exception as e:
            return False, f"Send error: {e}"
        finally:
            sock.close()
    
    def broadcast_message(self, subnet, text):
        success_count = 0
        base_ip = '.'.join(subnet.split('.')[:3])
        
        for i in range(1, 255):
            target_ip = f"{base_ip}.{i}"
            if target_ip != self.get_my_ip():
                success, _ = self.send_text(target_ip, text)
                if success:
                    success_count += 1
        
        return success_count
    
    def get_my_ip(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
        except:
            return "127.0.0.1"
        finally:
            sock.close()
    
    def check_port(self, ip, port=None):
        check_port = port or self.port
        try:
            sock = self.create_socket()
            sock.connect((ip, check_port))
            sock.close()
            return True
        except:
            return False

def quick_send(ip, message):
    core = VKMaxCore()
    return core.send_text(ip, message)

def quick_server():
    core = VKMaxCore()
    core.start_server()

if __name__ == "__main__":
    print("VKMax Core - base soket functions")
    print("Usage module: from vkmax_core import VKMaxCore")