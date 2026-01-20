import http.server
import socketserver
import os
import json

PORT = 8080
DIRECTORY = "C:\\Users\\groot\\Music\\susu\\Dummy-App"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Simulate API endpoints for dashboard.html
        if self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"users": 1024, "growth": "5%"}).encode())
            return
            
        elif self.path == '/api/notifications':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(["New login detected", "System update pending"]).encode())
            return

        return super().do_GET()

if __name__ == "__main__":
    # Change CWD to the app directory just in case
    if os.path.exists(DIRECTORY):
        os.chdir(DIRECTORY)
        
    print(f"Starting Dummy App Server at http://localhost:{PORT}")
    print(f"Serving directory: {DIRECTORY}")
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
