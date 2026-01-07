
import requests
import sys

try:
    response = requests.post(
        "http://localhost:8000/query",
        json={"question": "Hello, are you ready?"}
    )
    if response.status_code == 200:
        print("Success: Agent responded.")
        print("Response:", response.json())
    else:
        print(f"Failed: Status {response.status_code}")
        print("Detail:", response.text)
        sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
