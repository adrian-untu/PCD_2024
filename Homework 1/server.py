import socket
import argparse
import time

def tcp_server(port, buffer_size):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen()
        print(f"TCP Server listening on port {port}")
        conn, addr = s.accept()
        with conn:
            print(f'Connected by {addr}')
            total_data_received = 0
            start_time = time.time()
            while True:
                data = conn.recv(buffer_size)
                if not data:
                    break
                total_data_received += len(data)
            end_time = time.time()
            print(
                f'Protocol: TCP, Messages Read: {total_data_received / buffer_size}, Bytes Read: {total_data_received}, Time: {end_time - start_time}')


def udp_server(port, buffer_size):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', port))
        print(f"Server listening on port {port}")
        total_data_received = 0
        start_time = time.time()

        try:
            while True:
                data, addr = s.recvfrom(buffer_size)
                if not data:
                    break
                # print(f"Received data from {addr}")
                total_data_received += len(data)
                s.sendto(b"ACK", addr)  # Send ACK back to the client
                end_time = time.time()

        except KeyboardInterrupt:
            pass  # Allow server to be stopped with Ctrl+C
        print(
            f'Protocol: UDP, Messages Read: {total_data_received / buffer_size}, Bytes Read: {total_data_received}, Time: {end_time - start_time}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Server for TCP or UDP protocol.')
    parser.add_argument('--protocol', choices=['tcp', 'udp'], required=True, help='Protocol to use (tcp or udp)')
    parser.add_argument('--port', type=int, default=12345, help='Port number')
    parser.add_argument('--buffer_size', type=int, default=1024, help='Buffer size in bytes')
    args = parser.parse_args()

    if args.protocol == 'tcp':
        tcp_server(args.port, args.buffer_size)
    elif args.protocol == 'udp':
        udp_server(args.port, args.buffer_size)
