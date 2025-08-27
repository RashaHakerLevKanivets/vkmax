#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vkmax_core import VKMaxCore

class VKMaxClient:
    def __init__(self):
        self.core = VKMaxCore()
        self.running = True
    
    def show_help(self):
        print("\nCommands VKMax:")
        print("  /quit, /exit     -  exit")
        print("  /file <path>     -  send file")
        print("  /broadcast <msg> -  send to everyone on the network")
        print("  /check <IP>      -  check availability")
        print("  /help            -  print help")
        print("  /myip            -  show you IP")
        print("  Edit the code    -  if you want more features")
    
    def handle_command(self, command, target_ip=None):
        parts = command.split(' ', 1)
        cmd = parts[0].lower()
        
        if cmd in ['/quit', '/exit']:
            self.running = False
            return True, "Exit."
            
        elif cmd == '/file' and len(parts) > 1 and target_ip:
            return self.core.send_file(target_ip, parts[1])
            
        elif cmd == '/broadcast' and len(parts) > 1:
            count = self.core.broadcast_message(self.core.get_my_ip(), parts[1])
            return True, f"Sent to {count} nodes"
            
        elif cmd == '/check' and len(parts) > 1:
            if self.core.check_port(parts[1]):
                return True, f"{parts[1]} available"
            else:
                return False, f"{parts[1]} unavailable"
                
        elif cmd == '/myip':
            return True, f"IP: {self.core.get_my_ip()}"
            
        elif cmd == '/help':
            self.show_help()
            return True, ""
            
        return False, "Unknown key"
    
    def start_chat(self, server_ip):
        print(f"VKMax Connect. Connecting to {server_ip}")
        print("Type /help for help")
        
        while self.running:
            try:
                message = input("> ").strip()
                if not message:
                    continue
                
                is_command, result = self.handle_command(message, server_ip)
                if is_command:
                    if result:
                        print(result)
                    if not self.running:
                        break
                    continue
                
                success, result = self.core.send_text(server_ip, message)
                print(result)
                
            except KeyboardInterrupt:
                print("\nExit.")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def run(self):
        if len(sys.argv) < 2:
            print("Usage:")
            print("  Listen:       ./vkmax.py -l (tip - allow port for listening)")
            print("  Connect:      ./vkmax.py -c <IP_>")
            print("  Fast sending: ./vkmax.py -s <IP> <message>")
            return
        
        mode = sys.argv[1]
        
        if mode == '-l':
            self.core.start_server()
        elif mode == '-c' and len(sys.argv) >= 3:
            self.start_chat(sys.argv[2])
        elif mode == '-s' and len(sys.argv) >= 4:
            success, result = self.core.send_text(sys.argv[2], ' '.join(sys.argv[3:]))
            print(result)
        else:
            print("Key Error")

if __name__ == "__main__":
    client = VKMaxClient()
    client.run()