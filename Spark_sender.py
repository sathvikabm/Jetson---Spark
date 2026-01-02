import requests
import socket
import json

# Jetson configuration
JETSON_IP = "xxx.xxx.xxx.xx"  # Replace with your Jetson's actual IP
JETSON_PORT = 5001

def chat(
    text: str,
    model: str = "Qwen/Qwen2.5-Math-1.5B-Instruct",
    max_tokens: int = 500,
    base_url: str = "http://localhost:8000"
) -> str:
    """
    Send a message to the local LLM and get a response.
    """
    url = f"{base_url}/v1/chat/completions"
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": text}],
        "max_tokens": max_tokens
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    data = response.json()
    return data["choices"][0]["message"]["content"]

def send_to_jetson(query: str, response: str):
    """
    Send the LLM output to Jetson over Ethernet
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((JETSON_IP, JETSON_PORT))
            
            # Package the data as JSON
            message = {
                "query": query,
                "response": response
            }
            
            # Send the data
            s.sendall(json.dumps(message).encode())
            print(f"✓ Sent to Jetson at {JETSON_IP}:{JETSON_PORT}")
            
    except Exception as e:
        print(f"✗ Error sending to Jetson: {e}")

if __name__ == "__main__":
    # Test the function
    query = "12*17"
    result = chat(query)
    print(f"LLM Response: {result}")
    
    # Send to Jetson
    send_to_jetson(query, result)