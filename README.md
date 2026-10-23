# 🌐 WebOmni API — Universal Web Intelligence, x402 Gateway & MCP Server

[![OpenAPI 3.1](https://img.shields.io/badge/OpenAPI-3.1-brightgreen.svg)](https://github.com/whyst0ne/webomni-api)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![x402 Protocol](https://img.shields.io/badge/HTTP%20402-x402%20Base%20USDC-blue.svg)](https://github.com/whyst0ne/webomni-api)
[![MCP Ready](https://img.shields.io/badge/MCP-JSON--RPC%202.0-orange.svg)](https://modelcontextprotocol.io/)
[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-ea4aaa?style=flat&logo=github)](https://github.com/sponsors/whyst0ne)

**WebOmni API** is an autonomous micro-SaaS web intelligence, structured data extraction, smart-contract security scanner, and **HTTP 402 (`x402`) Micro-Payment Gateway** engineered for both human developers and autonomous AI agents.

---

## 🚀 Key Endpoints & Agent Capabilities

| Endpoint / Tool | Protocol | Description | Pricing / Access |
| :--- | :--- | :--- | :--- |
| `GET /api/v1/extract` | REST / OpenAPI 3.1 | Clean Markdown extraction, metadata scraping & DOM sanitization | Free Tier / API Key |
| `GET /api/v1/leads` | REST / JSON | Verified B2B tech founder & executive lead enrichment | Free Sample / Commercial |
| `GET /api/v1/flashloan-signal` | **x402 (`HTTP 402`)** | Live Base & Arbitrum DEX arbitrage spreads + Aave V3 `flashLoanSimple` ABI calldata | **0.05 USDC** (Base) |
| `POST /api/v1/audit-contract` | **x402 (`HTTP 402`)** | Automated Solidity / Node.js static vulnerability & CWE audit | **0.10 USDC** (Base) |
| `mcp_agent_server.py` | **MCP (JSON-RPC 2.0)** | Native tool interface (`get_live_flashloan_signals`, `audit_solidity_code`, `get_payment_instructions`) | Claude / Cursor / Agents |

---

## 🔗 x402 Machine-to-Machine Payment Flow
1. **Request Protected Resource:** Call `GET /api/v1/flashloan-signal` without a payment header.
2. **Receive `HTTP 402 Payment Required`:** Response includes exact Base USDC contract (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`) and recipient wallet `0xE5Ab26877172254B72f3AE6DA5789D2468B7B282`.
3. **Settle On-Chain & Unlock:** Submit the transaction hash via `X-Payment-TxHash: 0x...` to verify the on-chain `Transfer` event log and receive the unlocked payload immediately.

---

## 💳 Settlement & Enterprise Licensing
- **EVM Treasury & x402 Receiver (Base / Arbitrum / Optimism / Polygon / Ethereum):**  
  `0xE5Ab26877172254B72f3AE6DA5789D2468B7B282`
- **Companion Products:**  
  - [Crypto Arbitrage Scanner](https://github.com/whyst0ne/crypto-arbitrage-scanner)  
  - [B2B Tech Founders Leads Dataset](https://github.com/whyst0ne/b2b-tech-founders-leads)
