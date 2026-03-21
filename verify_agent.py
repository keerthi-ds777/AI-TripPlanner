
import requests
import sys
import json

try:
    response = requests.post(
        "http://localhost:8000/query",
        json={"question": "Hello, are you ready?"}
    )
    if response.status_code == 200:
        print("Success: Agent responded.")
        with open("last_success.txt", "w") as f:
            f.write(json.dumps(response.json(), indent=2))
    else:
        print(f"Failed: Status {response.status_code}")
        # Capture the detail from the JSON response if possible
        try:
            error_detail = response.json()
            print("Error Detail:", error_detail)
            with open("last_error.txt", "w") as f:
                f.write(json.dumps(error_detail, indent=2))
        except:
            print("Error Text:", response.text)
            with open("last_error.txt", "w") as f:
                f.write(response.text)
        sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    with open("last_error.txt", "w") as f:
        f.write(str(e))
    sys.exit(1)
