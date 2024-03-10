import socket
import time
import argparse


def tcp_client(server_ip, port, data, buffer_size):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, port))
        start_time = time.time()
        total_bytes_sent = 0
        for i in range(0, len(data), buffer_size):
            sent = s.send(data[i:i+buffer_size])
            total_bytes_sent += sent
        end_time = time.time()
        print(f'Transmission Time: {end_time - start_time} seconds, Messages Sent: {len(data) / buffer_size}, Bytes Sent: {total_bytes_sent}')

def udp_client_stop_and_wait(server_ip, port, data, buffer_size):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(2.0)  # Set a timeout for receiving ACKs
        total_bytes_sent = 0
        start_time = time.time()

        for i in range(0, len(data), buffer_size):
            message = data[i:i + buffer_size]
            while True:
                try:
                    s.sendto(message, (server_ip, port))
                    ack, _ = s.recvfrom(1024)  # Waiting for ACK
                    if ack == b"ACK":
                        total_bytes_sent += len(message)
                        break  # Move to next message after receiving ACK
                except socket.timeout:
                    print("ACK not received. Resending...")
                    continue  # Resend the same message if ACK not received within timeout

        end_time = time.time()
        print(f'UDP Stop-and-Wait Transmission Time: {end_time - start_time} seconds, Messages Sent: {len(data) // buffer_size}, Bytes Sent: {total_bytes_sent}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Client for TCP or UDP protocol.')
    parser.add_argument('--protocol', choices=['tcp', 'udp'], required=True, help='Protocol to use (tcp or udp)')
    parser.add_argument('--server_ip', default="127.0.0.1", help='Server IP address')
    parser.add_argument('--port', type=int, default=12345, help='Port number')
    parser.add_argument('--buffer_size', type=int, default=1024, help='Buffer size in bytes')
    args = parser.parse_args()

    # Example data payload; adjust as needed for your tests
    data = b"x" * 500000000  # For 500MB
    data1 = b"x" * 1000000000  # For 1GB
    data2 = b"x" * 100000000  # For 100MB

    if args.protocol == 'tcp':
        tcp_client(args.server_ip, args.port, data, args.buffer_size)
    elif args.protocol == 'udp':
        udp_client_stop_and_wait(args.server_ip, args.port, data, args.buffer_size)
