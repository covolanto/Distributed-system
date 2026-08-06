# time_server.py
# Save this in: Clock syncronizion/time_server.py

import socket
import time
import argparse

class TimeServer:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.running = True
        self.processing_delay = 0
        self.request_count = 0
        
    def start(self):
        """Start the time server"""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((self.host, self.port))
            sock.settimeout(1.0)
            
            print(f"🕐 TIME SERVER RUNNING")
            print(f"   Host: {self.host}")
            print(f"   Port: {self.port}")
            print(f"   Press Ctrl+C to stop\n")
            
            while self.running:
                try:
                    data, addr = sock.recvfrom(1024)
                    self.request_count += 1
                    
                    # Simulate server processing delay
                    if self.processing_delay > 0:
                        time.sleep(self.processing_delay / 1000.0)
                    
                    # Get current server time
                    server_time = time.time()
                    
                    # Send response
                    response = f"{server_time}"
                    sock.sendto(response.encode(), addr)
                    
                    print(f"   [Request #{self.request_count}] from {addr} → {server_time:.6f}")
                    
                except socket.timeout:
                    continue
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"   Error: {e}")
                    break
                    
    def stop(self):
        """Stop the server"""
        self.running = False
        
    def set_processing_delay(self, delay_ms):
        """Set artificial processing delay"""
        self.processing_delay = delay_ms
        print(f"   Processing delay set to {delay_ms}ms")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Time Server')
    parser.add_argument('--port', type=int, default=8000, help='Server port')
    parser.add_argument('--delay', type=int, default=0, help='Processing delay in ms')
    args = parser.parse_args()
    
    server = TimeServer(port=args.port)
    server.set_processing_delay(args.delay)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")
        server.stop()