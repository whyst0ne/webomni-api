import json
from main import app

with open("openapi.json", "w", encoding="utf-8") as f:
    json.dump(app.openapi(), f, indent=2)

print("[+] openapi.json generated successfully for RapidAPI import!")
