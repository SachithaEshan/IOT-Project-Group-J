from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse

HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 8081  # Port to listen on (make sure it's not being used by other services)
LOG_FILE = 'gps_log.txt'

# Print current working directory
current_directory = os.getcwd()
print("Current working directory:", current_directory)

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_data = urllib.parse.parse_qs(post_data.decode())
        latitude = parsed_data.get('lat')[0]
        longitude = parsed_data.get('lng')[0]
        speed = parsed_data.get('speed')[0]

        with open(LOG_FILE, 'a') as f:
            f.write(f"Latitude: {latitude}, Longitude: {longitude}, Speed: {speed}\n")
            print(f"Logged data - Latitude: {latitude}, Longitude: {longitude}, Speed: {speed}")

        self.send_response(200)
        self.end_headers()

def run_server(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = (HOST, PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Server listening on {HOST}:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
