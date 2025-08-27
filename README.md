
# VKMax - Simple messenger for local network

VKMax is a lightweight console messenger for exchanging text messages and files in a local network.

## Features

- 📨 Sending text messages
- 📁 Transferring files
- 🌐 Broadcasting messages
- 🔍 Checking the availability of nodes in the network
- 🖥️ Server mode for receiving messages

## Installation

1. Copy the `vkmax.py` and `vkmax_core.py` files to the desired directory
2. Make sure Python 3.x is installed
3. Allow connections through port 12345 in your firewall

## Usage

### Run in server mode (listening for messages):
```bash
./vkmax.py server
```

### Connect to another user:
```bash
./vkmax.py client <IP_address>
```

### Quickly send a message:
```bash
./vkmax.py send <IP_address> "Your message"
```

## Chat commands

- `/quit`, `/exit` - exit the program
- `/file <path>` - send a file
- `/broadcast <message>` - send a message to everyone in the network
- `/check <IP>` - check the availability of the node
- `/help` - show help on commands
- `/myip` - show your IP address

## Example of work

1. **User A** starts the server:
```bash
./vkmax.py server
```

2. **User B** connects to user A:
```bash
./vkmax.py client 192.168.1.100
```

3. **User B** sends a message:
```
> Hello! How are you?
```

4. **User A** sees the message:
```
[14:30] UserB: Hi! How are you?
```

## Technical details

- Default port: 12345 (TCP)
- Automatic IP address detection
- Nickname support (uses the system username)
- Connection timeout: 3 seconds

## Security

⚠️ **Warning**: VKMax does not use encryption and is intended for use in trusted local networks.

## Development

The project consists of two main modules:

- `vkmax.py` - client interface and command processing
- `vkmax_core.py` - basic socket functions and data transfer logic

To add new functions, edit the corresponding modules.

## Limitations

- Works only in IPv4 networks
- No group chat support
- No message history
- Basic error handling

## License

The project is distributed on an "as is" basis. You can modify it to suit your needs.