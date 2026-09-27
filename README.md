# Shoyaive AI

A personal AI assistant. **Phase 1** implements a basic AI chatbot with a
React frontend and a FastAPI backend. The architecture is designed so that
future capabilities — document analysis, RAG, web search, tool calling,
conversation history, authentication, and more — can be added as
independent modules without rewriting what's already here.

## Technologies

**Frontend:** React, Vite, JavaScript, Tailwind CSS
**Backend:** Python, FastAPI
**AI provider:** OpenAI API (swappable — see [Architecture](#architecture-notes))

## Folder structure

```
shoyaive-ai/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app wiring (CORS, routers) only
│   │   ├── config.py                # All environment configuration
│   │   ├── routes/
│   │   │   └── chat.py              # POST /api/chat — thin HTTP layer
│   │   ├── services/
│   │   │   ├── chat_service.py      # Chat business logic
│   │   │   ├── ai_service.py        # AI provider factory
│   │   │   └── providers/
│   │   │       ├── base.py          # AIProvider interface
│   │   │       └── openai_provider.py
│   │   ├── prompts/
│   │   │   └── system_prompt.py     # Shoyaive AI's system prompt
│   │   ├── schemas/
│   │   │   └── chat.py              # Request/response validation
│   │   ├── models/                  # (empty) future DB models
│   │   └── tools/                   # (empty) future AI tools
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    └── src/
        ├── components/
        │   ├── chat/                 # ChatWindow, MessageBubble, MessageInput, ...
        │   └── layout/                # TopBar
        ├── layouts/
        │   └── MainLayout.jsx
        ├── pages/
        │   └── ChatPage.jsx
        ├── hooks/
        │   └── useChat.js             # All chat state/logic
        ├── services/api/
        │   ├── apiClient.js           # Generic fetch wrapper
        │   └── chatService.js         # Chat-specific API calls
        ├── constants/
        │   └── config.js
        └── utils/
            └── id.js
```

## Installation

Requires **Node.js 18+** and **Python 3.10+**.

### 1. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Frontend

```bash
cd frontend
npm install
```

## Environment setup

### Backend (`backend/.env`)

Copy the example file and fill in your OpenAI key:

```bash
cd backend
cp .env.example .env
```

```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...your-key-here...
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1000

HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development

CORS_ORIGINS=http://localhost:5173
```

The server **will not start** if `OPENAI_API_KEY` is missing — this is
intentional, so misconfiguration fails immediately instead of silently at
the first chat request.

### Frontend (`frontend/.env`)

```bash
cd frontend
cp .env.example .env
```

```env
VITE_API_URL=http://localhost:8000
```

## Running the app

### Start the backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Start the frontend

In a separate terminal:

```bash
cd frontend
npm run dev
```

Open the URL Vite prints (typically **http://localhost:5173**).

## Testing the chatbot

1. With both servers running, open the frontend in your browser.
2. Type a message and press **Enter** (or click send).
3. You should see your message appear, a loading indicator, then the AI's
   reply.

You can also test the backend directly:

```bash
# Health check
curl http://localhost:8000/api/health

# Chat request
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello!"}]}'
```

Interactive API docs are available at **http://localhost:8000/docs**
(FastAPI's built-in Swagger UI) once the backend is running.

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| Backend refuses to start with an `OPENAI_API_KEY is not set` error | Create `backend/.env` from `.env.example` and add a real key. |
| Frontend shows "Could not reach the server" | Backend isn't running, or is on a different port than `VITE_API_URL` in `frontend/.env`. |
| Browser console shows a CORS error | Add the frontend's origin (e.g. `http://localhost:5173`) to `CORS_ORIGINS` in `backend/.env`, then restart the backend. |
| Chat request returns `502 Bad Gateway` | The OpenAI API call failed — check your API key, account credits/quota, and that `api.openai.com` is reachable from your network. |
| Chat request returns `422 Unprocessable Entity` | The request body didn't match the expected schema (e.g. empty `messages` array). |
| `pip install` fails | Confirm you're using Python 3.10+ and that your virtual environment is activated. |
| `npm install` / `npm run dev` fails | Confirm you're using Node.js 18+. Delete `node_modules` and `package-lock.json` and reinstall if issues persist. |

## Architecture notes

- **Swapping AI providers:** `services/ai_service.py` is the only place
  that knows how to construct a provider. To add Anthropic, a local model,
  etc., implement the `AIProvider` interface (`services/providers/base.py`)
  in a new file, register it in `_PROVIDERS`, and set `AI_PROVIDER` in
  `.env`. Nothing else in the app needs to change.
- **Adding future features** (summarization, PDF/DOCX upload, RAG, web
  search, calculator, tool calling, etc.): add a new route + service +
  schema following the same pattern as `chat`, and a new tool file under
  `app/tools/` once tool calling is introduced. The frontend follows the
  same rule — a new feature gets its own service file under
  `src/services/api/` and its own components/hooks, without modifying the
  chat feature.
- **Statelessness (Phase 1):** the backend holds no conversation state —
  the frontend sends the full message history on every request. This
  keeps Phase 1 simple and leaves room to add persistence (PostgreSQL,
  conversation history) later without breaking the API contract (just add
  an optional `conversation_id` field).

## What's not implemented yet

By design, Phase 1 does **not** include: file uploads, document analysis,
RAG, a personal knowledge base, web search, a calculator, tool calling,
conversation history/persistence, or authentication. The architecture
above exists specifically so these can be added incrementally.
