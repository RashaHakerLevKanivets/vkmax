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
        print("\nКоманды VKMax:")
        print("  /quit, /exit    - выход")
        print("  /file <путь>    - отправить файл")
        print("  /broadcast <msg>- отправить всем в сети")
        print("  /check <IP>     - проверить доступность")
        print("  /help           - эта справка")
        print("  /myip           - показать мой IP")
    
    def handle_command(self, command, target_ip=None):
        parts = command.split(' ', 1)
        cmd = parts[0].lower()
        
        if cmd in ['/quit', '/exit']:
            self.running = False
            return True, "Выход"
            
        elif cmd == '/file' and len(parts) > 1 and target_ip:
            return self.core.send_file(target_ip, parts[1])
            
        elif cmd == '/broadcast' and len(parts) > 1:
            count = self.core.broadcast_message(self.core.get_my_ip(), parts[1])
            return True, f"Отправлено {count} узлам"
            
        elif cmd == '/check' and len(parts) > 1:
            if self.core.check_port(parts[1]):
                return True, f"{parts[1]} доступен"
            else:
                return False, f"{parts[1]} недоступен"
                
        elif cmd == '/myip':
            return True, f"Мой IP: {self.core.get_my_ip()}"
            
        elif cmd == '/help':
            self.show_help()
            return True, ""
            
        return False, "Неизвестная команда"
    
    def start_chat(self, server_ip):
        print(f"VKMax Client. Подключение к {server_ip}")
        print("Введите /help для списка команд")
        
        while self.running:
            try:
                message = input("> ").strip()
                if not message:
                    continue
                
                # Обрабатываем команды
                is_command, result = self.handle_command(message, server_ip)
                if is_command:
                    if result:
                        print(result)
                    if not self.running:
                        break
                    continue
                
                # Отправляем обычное сообщение
                success, result = self.core.send_text(server_ip, message)
                print(result)
                
            except KeyboardInterrupt:
                print("\nВыход.")
                break
            except Exception as e:
                print(f"Ошибка: {e}")
    
    def run(self):
        if len(sys.argv) < 2:
            print("Использование:")
            print("  Сервер: ./vkmax.py server")
            print("  Клиент: ./vkmax.py client <IP_сервера>")
            print("  Быстрая отправка: ./vkmax.py send <IP> <сообщение>")
            return
        
        mode = sys.argv[1]
        
        if mode == 'server':
            self.core.start_server()
        elif mode == 'client' and len(sys.argv) >= 3:
            self.start_chat(sys.argv[2])
        elif mode == 'send' and len(sys.argv) >= 4:
            success, result = self.core.send_text(sys.argv[2], ' '.join(sys.argv[3:]))
            print(result)
        else:
            print("Неверные аргументы")

if __name__ == "__main__":
    client = VKMaxClient()
    client.run()