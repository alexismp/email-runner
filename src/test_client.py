
import base64
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

# Get the file path from the command-line arguments
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    sys.exit(1)

# Read the image file and encode it in base64
with open(file_path, "rb") as f:
    image_bytes = f.read()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

# Prepare the request payload
payload = {"name": os.path.basename(file_path), "image": encoded_image}

# Get the API key from the environment
api_key = os.environ.get("API_KEY")
if not api_key:
    print("Error: API_KEY not found in environment variables.")
    sys.exit(1)

headers = {"X-API-KEY": api_key}

# Send the request to the /upload endpoint
try:
    response = requests.post(
        "http://127.0.0.1:8080/upload", json=payload, headers=headers
    )
    response.raise_for_status()  # Raise an exception for bad status codes
    print(response.text)
except requests.exceptions.RequestException as e:
    print(f"Error sending request: {e}")
