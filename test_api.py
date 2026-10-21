import sys
from fastapi.testclient import TestClient
from main import app

sys.stdout.reconfigure(encoding='utf-8')

client = TestClient(app)

def test_endpoints():
    print("[*] 1. Testing /health endpoint...")
    resp = client.get("/health")
    assert resp.status_code == 200, f"Health check failed: {resp.text}"
    print("   [+] Health response:", resp.json())

    print("\n[*] 2. Testing /api/v1/extract endpoint (using example.com)...")
    resp = client.post("/api/v1/extract", json={"url": "https://example.com"})
    assert resp.status_code == 200, f"Extract failed: {resp.text}"
    data = resp.json()
    print("   [+] Title:", data.get("title"))
    print("   [+] Word count:", data.get("metrics", {}).get("word_count"))
    print("   [+] Tokens:", data.get("metrics", {}).get("estimated_llm_tokens"))

    print("\n[*] 3. Testing /api/v1/seo-audit endpoint (using example.com)...")
    resp = client.post("/api/v1/seo-audit", json={"url": "https://example.com"})
    assert resp.status_code == 200, f"SEO audit failed: {resp.text}"
    seo_data = resp.json()
    print("   [+] SEO Score:", seo_data.get("seo_score"))
    print("   [+] Recommendations:", seo_data.get("recommendations"))

    print("\n[SUCCESS] All WebOmni Micro-SaaS endpoints verified and functioning perfectly!")

if __name__ == "__main__":
    test_endpoints()
