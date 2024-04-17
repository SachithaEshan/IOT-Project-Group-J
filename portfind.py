import socket
import errno  # Import errno module for error handling

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            return True
        except OSError as e:
            if e.errno == errno.EADDRINUSE:  # Use errno for error code comparison
                return False
            else:
                raise  # Re-raise the exception if it's not EADDRINUSE

# Test ports 8080 to 8090
for port in range(8080, 8091):
    if check_port(port):
        print(f"Port {port} is available")
