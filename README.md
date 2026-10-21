# 🚀 WebOmni API — Universal Extraction & Web Intelligence Micro-SaaS

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?logo=python)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-throughput, low-latency Micro-SaaS API engine built for AI Agents, autonomous scrapers, LLM pipelines, and automated B2B research.

---

## ⚡ Key Features

- 📑 **Clean Content & Markdown Extractor**: Strips boilerplate, ads, scripts, and navigation to yield pristine markdown formatted for LLM consumption.
- 🎯 **Lead & Contact Intelligence**: Automatically scans web pages for email addresses, international phone numbers, and social links (LinkedIn, Twitter/X, GitHub, Discord, Telegram, YouTube).
- 🔍 **Real-Time Technical SEO Audit**: Evaluates meta title, description, OpenGraph tags, canonicals, H1-H6 hierarchy, viewport tags, and image alt attributes with an algorithmic health score (0-100).
- 🛡️ **Built-in Resiliency**: Emulates modern desktop user-agents, respects timeouts, and protects against memory exhaustion (5MB max stream cap).
- 🔌 **RapidAPI & Postman Ready**: Bundled with OpenAPI 3.1 schema for one-click marketplace deployment.

---

## 📡 API Endpoints

### 1. Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "engine": "WebOmni Micro-SaaS API",
  "version": "1.0.0"
}
```

---

### 2. Extract Clean Text & Markdown
```http
POST /v1/extract
Content-Type: application/json

{
  "url": "https://example.com",
  "extract_markdown": true,
  "include_meta": true
}
```

---

### 3. Extract B2B Leads & Socials
```http
POST /v1/leads
Content-Type: application/json

{
  "url": "https://company.com"
}
```
**Response:**
```json
{
  "target_url": "https://company.com",
  "emails": ["contact@company.com", "press@company.com"],
  "phones": ["+1-800-555-0199"],
  "social_profiles": {
    "linkedin": ["https://linkedin.com/company/example"],
    "twitter": ["https://x.com/example"],
    "github": ["https://github.com/example"]
  },
  "total_leads_found": 5
}
```

---

### 4. Technical SEO Audit
```http
POST /v1/seo
Content-Type: application/json

{
  "url": "https://example.com"
}
```
**Response:**
```json
{
  "target_url": "https://example.com",
  "seo_score": 92,
  "title": "Example Domain",
  "meta_description": "...",
  "headings": {
    "h1_count": 1,
    "h2_count": 3
  },
  "audit": {
    "has_title": true,
    "has_description": true,
    "has_viewport": true,
    "missing_alt_images_count": 0
  }
}
```

---

## 🛠️ Quickstart

### Run with Python
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Run with Docker
```bash
docker build -t webomni-api .
docker run -p 8000:8000 webomni-api
```

---

## 💎 Commercial Monetization Plans (RapidAPI)

| Plan | Price | Monthly Quota | Features |
|---|---|---|---|
| **Free Tier** | $0/mo | 100 requests | Rate-limited (5 req/min) |
| **Pro Tier** | $19/mo | 25,000 requests | Priority processing, unthrottled |
| **Ultra Tier** | $49/mo | 100,000 requests | Full concurrent access & lead enrichment |

---

## 📄 License
MIT License. Created by [whyst0ne](https://github.com/whyst0ne).
