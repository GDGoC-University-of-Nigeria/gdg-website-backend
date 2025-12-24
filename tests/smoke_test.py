import requests
import sys

def test_auth_endpoint():
    url = "http://localhost:8000/auth/google"
    payload = {"id_token": "invalid_token_for_smoke_test"}
    
    try:
        print(f"Sending POST to {url}...")
        response = requests.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        # We expect 401 or 500 depending on how validation fails, but definitely not 404
        if response.status_code == 401:
            print("Success! Endpoint reachable and rejecting invalid token locally.")
        elif response.status_code == 404:
            print("FAILURE: Endpoint not found.")
            sys.exit(1)
        else:
            print(f"Result: {response.status_code} - Likely reachable but different error.")
            
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_auth_endpoint()
