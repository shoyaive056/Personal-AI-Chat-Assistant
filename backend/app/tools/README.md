# tools/

Individual AI-callable capabilities (calculator, web search, PDF reading,
knowledge-base search, etc.) will live here, one file per tool — for
example `summarizer.py`, `calculator.py`, `web_search.py`.

Not implemented in Phase 1. When tool calling is added, each tool should
expose a plain function plus a schema describing its inputs, and
`services/ai_service.py` will be extended to pass the active tool set to
the provider rather than changing how routes or `ChatService` work.
