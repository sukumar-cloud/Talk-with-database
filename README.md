# Talk-with-database
An AI-powered assistant to talk to your databases using natural language. It supports intent understanding, SQL generation, validation, ranking, and execution. A modern React UI provides a chat experience and database workbenches.

![status](https://img.shields.io/badge/status-active-brightgreen)
![backend](https://img.shields.io/badge/backend-FastAPI-009485)
![frontend](https://img.shields.io/badge/frontend-React-61DAFB)
![license](https://img.shields.io/badge/license-Custom-lightgrey)

> Tip: Use the Quick Links below to jump directly to what you need.

## Quick Links
- **[Run Backend](#backend-setup)**
- **[Run Frontend](#frontend-setup)**
- **[Try the Chat API (cURL)](#api-playground)**
- **[Swagger Docs](#api-documentation)** (`/docs`)
- **[Troubleshooting](#troubleshooting)**

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [API Documentation](#api-documentation)
- [API Playground](#api-playground)
- [Using the Chatbot](#using-the-chatbot)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🧠 Features
- **Natural language to SQL**: Generate safe, executable queries from user prompts.
- **Safety & ranking**: Validate generated SQL and rank candidates before execution.
- **Execution & results**: Run queries and return concise results.
- **Schema inspection**: Inspect MySQL schema (and MongoDB via dedicated routes).
- **Chat UI**: Friendly chatbot page with loading/error states.

## 🏗️ Architecture
- **Frontend**: React + Vite + Tailwind (`project/`)
- **Backend**: FastAPI (`backend/fastapi_app/`)
- **Routers**: `nlu`, `generate`, `validate`, `rank`, `execute`, `schema`, `mongodb`, `history`, `chat`

```mermaid
flowchart LR
  A[User Prompt] --> B(Chat UI)
  B --> C[/POST /chat/]
  C --> D[NLU]
  C --> E[Generate]
  C --> F[Validate]
  C --> G[Rank]
  C --> H[Execute]
  H --> I[(DB)]
  H --> J[Results]
  J --> B
```

## 🧰 Tech Stack
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009485?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind-06B6D4?logo=tailwindcss&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)
- Frontend: React, TypeScript, Vite, TailwindCSS, lucide-react
- Backend: FastAPI, Uvicorn, Pydantic, SQLAlchemy, PyMySQL, PyMongo
- Optional: spaCy (NLU), sentence-transformers/transformers (depending on generator)

## ✅ Prerequisites
- Node.js 18+
- Python 3.10+
- A MySQL database (for SQL features)
- Optionally MongoDB (for Mongo routes)

## ⚙️ Backend Setup
<details>
<summary><b>Show steps</b></summary>

```bash
cd backend
python -m venv .venv
\\.venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```

Create `backend/.env` and set at least:
```
DB_TYPE=mysql
DB_URI=mysql+pymysql://USER:PASSWORD@HOST:PORT/DBNAME

# Optional generator settings
GENERATOR_PROVIDER=mixtral
GENERATOR_N_CANDIDATES=5
GENERATOR_TEMPERATURE=0.2
GENERATOR_TOP_P=0.95
GENERATOR_MAX_TOKENS=200

# For Mongo features
# MONGO_URI=mongodb://user:pass@host:27017
```

Run the API:
```bash
uvicorn fastapi_app.main:app --reload --host 0.0.0.0 --port 8000
```

</details>

## 💻 Frontend Setup
<details>
<summary><b>Show steps</b></summary>

```bash
cd project
npm install
```

Configure API base (optional). Create `project/.env`:
```
VITE_API_BASE=http://127.0.0.1:8000
```

Run the dev server:
```bash
npm run dev
```

Open the app and navigate to `http://localhost:5173/chatbot` (or your Vite dev URL).

</details>

## 🔌 Key Endpoints (Backend)
- `POST /chat/` — Unified chat: intent → generate → validate → rank → execute
- `POST /schema/inspect` — Inspect MySQL schema (or MongoDB via env)
- `POST /nlu/parse` — Intent + entities + dependencies
- `POST /generate/` — Generate SQL candidates
- `POST /validate/` — Validate SQL candidates
- `POST /rank/` — Rank SQL candidates
- `POST /execute/` — Execute SQL
- `POST /mongodb/*` — MongoDB NLU, generate, validate, execute
- `GET /history/*` — Query history ops

## 📚 API Documentation
- Open Swagger UI at: `http://127.0.0.1:8000/docs`
- Open ReDoc at: `http://127.0.0.1:8000/redoc`

## 🧪 API Playground
Try these once the backend is running.

```bash
# 1) Inspect schema
curl -s -X POST http://127.0.0.1:8000/schema/inspect -H "Content-Type: application/json" -d "{}" | jq

# 2) Ask a question via Chat API
curl -s -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" \
  -d '{
    "text": "Show last 10 customers by signup date",
    "db_type": "mysql"
  }' | jq

# 3) Direct SQL execution (advanced)
curl -s -X POST http://127.0.0.1:8000/execute -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT * FROM customers LIMIT 5",
    "db_type": "mysql"
  }' | jq
```

## 🤖 Using the Chatbot
1. Ensure backend is running and `DB_URI` is valid.
2. Open the Chatbot page.
3. Ask questions like:
   - "Show last 10 customers by signup date"
   - "Total revenue per month in 2024"
4. The bot will reply with detected intent, best SQL, and a summary of results.

### Sample Prompts
- "Top 5 products by sales in Q2"
- "List customers who placed more than 3 orders in the last 30 days"
- "Average order amount per customer"

### Tips
- Be specific about time ranges and sorting. Example: "last 30 days", "order by created_at desc".
- If you see no results, try a simpler version first.

## 🛠️ Troubleshooting
- **Bot stuck on “Thinking…”**
  - Verify backend logs. Confirm `VITE_API_BASE` points to the API URL.
  - Check CORS and that the backend is reachable at `http://127.0.0.1:8000`.
- **`DB_URI not set`**
  - Add `DB_URI` to `backend/.env` and restart Uvicorn.
- **No rows returned / errors**
  - Validate schema is correct; try simpler queries.
- **Generator configuration**
  - If using an external LLM provider in `core.generator`, ensure required API keys are configured.
 - **MongoDB features**
   - Ensure `MONGO_URI` is set and use the `/mongodb/*` endpoints.

## 👩‍💻 Development
- Frontend code: `project/src/`
- Backend routers: `backend/fastapi_app/routers/`
- Start backend and frontend in separate terminals for live reload.

## 🤝 Contributing
1. Create a feature branch.
2. Commit with clear messages.
3. Open a PR describing changes and testing steps.

## 📜 License
This repository may include third-party dependencies with their own licenses. Add a LICENSE file if you plan to open-source under a specific license.
