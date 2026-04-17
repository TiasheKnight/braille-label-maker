"""Web handler for MicroPython ESP32"""

import socket
import time
from handlers import print_handler, vibration


def create_html():
    """Create the HTML page"""
    return """
    <html>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Braille Label Maker</title>
        <style>body{font-family:Arial,sans-serif;margin:24px;}input{width:90%;padding:10px;}button{padding:10px 16px;}</style>
      </head>
      <body>
        <h2>Braille Label Maker</h2>
        <form action="/print" method="GET">
          <input name="text" placeholder="Enter text" autocomplete="off" />
          <button type="submit">Print</button>
        </form>
      </body>
    </html>
    """


def start_web_server(port=80):
    """Start simple HTTP web server"""
    addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)
    server.listen(1)
    
    print(f"Web server listening on port {port}")
    
    while True:
        try:
            client, addr = server.accept()
            request = client.recv(1024).decode()
            
            if "GET / " in request:
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{create_html()}"
                client.send(response.encode())
            
            elif "GET /print?" in request:
                # Parse the query string
                try:
                    start = request.find("text=") + 5
                    end = request.find(" ", start)
                    if end == -1:
                        end = request.find("\r", start)
                    
                    text = request[start:end]
                    text = text.replace("+", " ").replace("%20", " ")  # URL decode
                    
                    vibration.notify_command_received()
                    print_handler.print_text(text)
                    
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><p>Printed: {text}</p><p><a href=\"/\">Back</a></p></body></html>"
                except Exception as e:
                    print(f"Error: {e}")
                    response = "HTTP/1.1 400 Bad Request\r\n\r\nError processing request"
                
                client.send(response.encode())
            
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\nNot found"
                client.send(response.encode())
            
            client.close()
        
        except Exception as e:
            print(f"Server error: {e}")
            time.sleep_ms(100)


def init():
    """Initialize web server (non-blocking stub)"""
    print("Web handler initialized")
    # Note: call start_web_server() from main to actually start the server
