# time_client.py
# Save this in: Clock syncronizion/time_client.py

import socket
import time
import random
import statistics
import argparse

class TimeClient:
    def __init__(self, client_id, server_host='localhost', server_port=8000):
        self.client_id = client_id
        self.server_host = server_host
        self.server_port = server_port
        
        # Initialize local clock with random offset
        self.local_clock = time.time() + random.uniform(-5, 5)
        self.drift_rate = random.uniform(-0.0001, 0.0001)
        
        # Statistics
        self.sync_history = []
        self.rtt_history = []
        self.error_history = []
        self.total_syncs = 0
        
        print(f"👤 CLIENT {client_id} INITIALIZED")
        print(f"   Server: {server_host}:{server_port}")
        print(f"   Initial local time: {self.local_clock:.6f}")
    
    def get_local_time(self):
        """Get current local time with drift"""
        self.local_clock += self.drift_rate * 0.1
        return self.local_clock
    
    def synchronize(self):
        """Perform ONE synchronization cycle"""
        self.total_syncs += 1
        
        # Record request send time
        request_send_time = self.get_local_time()
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(2.0)
            
            try:
                # Send request
                sock.sendto(b"SYNC", (self.server_host, self.server_port))
                
                # Receive response
                data, _ = sock.recvfrom(1024)
                server_time = float(data.decode())
                
                # Record response receive time
                response_recv_time = self.get_local_time()
                
                # Calculate RTT
                rtt = response_recv_time - request_send_time
                self.rtt_history.append(rtt)
                
                # Calculate clock adjustment
                propagation_delay = rtt / 2
                adjusted_server_time = server_time + propagation_delay
                adjustment = adjusted_server_time - self.get_local_time()
                
                # Apply adjustment
                self.local_clock += adjustment
                
                # Record statistics
                error = abs(self.local_clock - server_time)
                self.error_history.append(error)
                
                print(f"   [{self.client_id}] Sync #{len(self.sync_history)+1}: "
                      f"RTT={rtt*1000:.1f}ms, Adj={adjustment*1000:.1f}ms, Error={error*1000:.1f}ms")
                
                return {
                    'success': True,
                    'rtt': rtt,
                    'adjustment': adjustment,
                    'error': error
                }
                
            except socket.timeout:
                print(f"   [{self.client_id}] ❌ TIMEOUT")
                return {'success': False, 'error': 'Timeout'}
            except Exception as e:
                print(f"   [{self.client_id}] ❌ ERROR: {e}")
                return {'success': False, 'error': str(e)}
    
    def run_continuous_sync(self, interval=2, duration=30):
        """Run continuous synchronization"""
        print(f"\n🔄 CLIENT {self.client_id} - Continuous Sync")
        print(f"   Interval: {interval}s, Duration: {duration}s")
        print("-" * 50)
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            self.synchronize()
            time.sleep(interval)
        
        self.print_summary()
    
    def print_summary(self):
        """Print synchronization summary"""
        if not self.error_history:
            print(f"[CLIENT {self.client_id}] No sync data available")
            return
            
        print(f"\n📊 CLIENT {self.client_id} - SUMMARY")
        print("=" * 50)
        print(f"Total syncs: {len(self.error_history)}")
        
        if self.error_history:
            print(f"\nError Statistics:")
            print(f"  Min: {min(self.error_history)*1000:.2f}ms")
            print(f"  Max: {max(self.error_history)*1000:.2f}ms")
            print(f"  Avg: {statistics.mean(self.error_history)*1000:.2f}ms")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Time Client')
    parser.add_argument('--id', type=int, default=1, help='Client ID')
    parser.add_argument('--server', default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8000, help='Server port')
    parser.add_argument('--interval', type=float, default=2, help='Sync interval')
    parser.add_argument('--duration', type=int, default=30, help='Run duration')
    args = parser.parse_args()
    
    client = TimeClient(args.id, args.server, args.port)
    client.run_continuous_sync(interval=args.interval, duration=args.duration)