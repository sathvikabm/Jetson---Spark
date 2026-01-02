import socket
import json

HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5001

def start_jetson_server():
    """
    Run this on Jetson to receive LLM outputs from Spark
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Jetson listening on {HOST}:{PORT}...")
        
        while True:
            conn, addr = s.accept()
            print(f"Connection from Spark: {addr}")
            
            with conn:
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    
                    # Decode the received data
                    try:
                        message = json.loads(data.decode())
                        print("\n=== Received from Spark ===")
                        print(f"Query: {message['query']}")
                        print(f"Response: {message['response']}")
                        print("=" * 30)
                        
                        #Processing done here 
                        
                    except json.JSONDecodeError:
                        print("RX:", data.decode(errors="replace"))

if __name__ == "__main__":
    start_jetson_server()