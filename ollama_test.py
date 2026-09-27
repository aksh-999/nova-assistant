import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2:3b",
        "prompt": "You are Nova, a helpful personal voice assistant. Say hello to me.",
        "stream": False
    }
)

data = response.json()

print("Nova:")
print(data["response"])