import re
import math
import urllib.request
import urllib.parse
from typing import Optional, List, Dict, Any
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

app = FastAPI(
    title="WebOmni API - Universal Extraction & Web Intelligence",
    description="High-performance, zero-overhead Web Content, SEO & Lead Intelligence API. Designed for AI agents, LLM pipelines, and automated research.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

class ExtractRequest(BaseModel):
    url: str
    extract_markdown: bool = True
    include_meta: bool = True

class LeadRequest(BaseModel):
    url: str

class SeoRequest(BaseModel):
    url: str

def fetch_html(target_url: str) -> str:
    parsed = urllib.parse.urlparse(target_url)
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="Only HTTP/HTTPS URLs are supported.")
    
    req = urllib.request.Request(
        target_url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            content_type = response.headers.get("content-type", "").lower()
            if "text/html" not in content_type and "application/xhtml" not in content_type:
                # Still try to read if text
                pass
            raw_bytes = response.read(1024 * 1024 * 5) # Max 5MB
            return raw_bytes.decode("utf-8", errors="replace")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch remote webpage: {str(e)}")

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "service": "WebOmni API",
        "version": "1.0.0",
        "pricing_model": "Pay-per-request / Monthly Tier"
    }

@app.post("/api/v1/extract")
def extract_content(req: ExtractRequest):
    html = fetch_html(req.url)
    soup = BeautifulSoup(html, "html.parser")

    # Clean scripts, styles, iframes, ads
    for tag in soup(["script", "style", "noscript", "svg", "iframe", "nav", "footer"]):
        tag.decompose()

    # Meta extraction
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_desc = ""
    desc_tag = soup.find("meta", attrs={"name": re.compile(r"description", re.I)}) or soup.find("meta", attrs={"property": "og:description"})
    if desc_tag and desc_tag.get("content"):
        meta_desc = desc_tag["content"].strip()

    og_image = ""
    img_tag = soup.find("meta", attrs={"property": "og:image"})
    if img_tag and img_tag.get("content"):
        og_image = img_tag["content"].strip()

    # Body extraction & formatting
    body_node = soup.body or soup
    text = body_node.get_text(separator="\n", strip=True)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    clean_text = "\n\n".join(lines)

    words = clean_text.split()
    word_count = len(words)
    reading_time_min = max(1, math.ceil(word_count / 220))
    approx_tokens = int(word_count * 1.33)

    return {
        "url": req.url,
        "title": title,
        "meta_description": meta_desc,
        "og_image": og_image,
        "metrics": {
            "word_count": word_count,
            "reading_time_minutes": reading_time_min,
            "estimated_llm_tokens": approx_tokens
        },
        "content": clean_text[:50000] # Safe return length
    }

@app.post("/api/v1/leads")
def extract_leads(req: LeadRequest):
    html = fetch_html(req.url)
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    # Extract emails
    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    emails = list(set(re.findall(email_regex, text)))

    # Extract phone numbers
    phone_regex = r'(\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4})'
    raw_phones = re.findall(phone_regex, text)
    phones = list(set([p.strip() for p in raw_phones if len(re.sub(r'\D', '', p)) >= 9]))

    # Social links
    socials: Dict[str, List[str]] = {
        "twitter": [],
        "linkedin": [],
        "github": [],
        "instagram": [],
        "youtube": []
    }
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if "twitter.com/" in href or "x.com/" in href:
            socials["twitter"].append(href)
        elif "linkedin.com/" in href:
            socials["linkedin"].append(href)
        elif "github.com/" in href:
            socials["github"].append(href)
        elif "instagram.com/" in href:
            socials["instagram"].append(href)
        elif "youtube.com/" in href:
            socials["youtube"].append(href)

    for k in socials:
        socials[k] = list(set(socials[k]))

    return {
        "url": req.url,
        "total_emails_found": len(emails),
        "emails": emails,
        "phones": phones[:10],
        "social_profiles": socials
    }

@app.post("/api/v1/seo-audit")
def audit_seo(req: SeoRequest):
    html = fetch_html(req.url)
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    desc_tag = soup.find("meta", attrs={"name": re.compile(r"description", re.I)})
    description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""

    h1_tags = [h.get_text(strip=True) for h in soup.find_all("h1")]
    h2_tags = [h.get_text(strip=True) for h in soup.find_all("h2")]

    images = soup.find_all("img")
    missing_alt = [img.get("src", "") for img in images if not img.get("alt")]

    score = 100
    recommendations = []

    if not title:
        score -= 25
        recommendations.append("Missing <title> tag.")
    elif len(title) < 20 or len(title) > 70:
        score -= 10
        recommendations.append(f"Title length ({len(title)} chars) should ideally be between 30 and 60 characters.")

    if not description:
        score -= 20
        recommendations.append("Missing meta description.")
    elif len(description) < 50 or len(description) > 160:
        score -= 10
        recommendations.append(f"Meta description length ({len(description)} chars) is outside optimal 70-155 range.")

    if len(h1_tags) == 0:
        score -= 15
        recommendations.append("No <h1> tag found on page.")
    elif len(h1_tags) > 1:
        score -= 5
        recommendations.append("Multiple <h1> tags found; best practice is exactly one primary H1.")

    if missing_alt:
        score -= min(15, len(missing_alt) * 3)
        recommendations.append(f"{len(missing_alt)} images are missing alt attributes.")

    return {
        "url": req.url,
        "seo_score": max(0, score),
        "title": title,
        "meta_description": description,
        "headings": {
            "h1_count": len(h1_tags),
            "h1_list": h1_tags,
            "h2_count": len(h2_tags)
        },
        "images": {
            "total_count": len(images),
            "missing_alt_count": len(missing_alt)
        },
        "recommendations": recommendations
    }

if __name__ == "__main__":
    import uvicorn
    print("[*] Starting WebOmni Micro-SaaS Server on port 8000...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
