# Study Assistant — AI-Powered PDF Note & Doubt Solver

A Django-based study assistant that converts uploaded PDFs into structured notes and provides contextual AI chat for doubt solving using Retrieval-Augmented Generation (RAG). The system combines document processing, vector search, and conversational AI into a clean web interface.

## Demo

**Live Demo:** https://study-assistant-t0hd.onrender.com

---

## Key Features

- PDF upload and automatic text extraction
- AI-generated structured notes from uploaded content
- Context-aware doubt solving via RAG-based chat
- Per-note chat history with conversational memory
- Vector embeddings stored per document chunk
- Custom authentication system with OTP email verification
- Google OAuth login via django-allauth
- User profiles with API key management
- Personal note history dashboard

---

## Tech Stack

- **Backend:** Django 6
- **Auth:** Custom Django auth + django-allauth (Google OAuth)
- **AI/LLM:** Google Gemini (LangChain integration)
- **Vector Search:** FAISS + NumPy
- **Document Processing:** PyPDF
- **Database:** Django ORM (PostgreSQL-ready)
- **Frontend:** Django templates + AJAX
- **Deployment:** Gunicorn / ASGI-compatible stack

---

## Architecture Overview

The project follows a modular Django architecture with two main apps:

### `authentication/`

Handles identity and user management:

- Custom `User` model extending Django auth
- `Profile` model for extended user data and API keys
- OTP-based email registration flow
- Google OAuth integration via custom social adapter
- Login, profile completion, and session management

### `notes/`

Core AI and document processing engine:

- `Note` model stores extracted PDF content and generated notes
- `Chunk` model stores document segments and embeddings
- `Chat` model stores conversational history per note
- RAG utilities for chunking, embedding, and retrieval
- AI note generation and contextual chat responses
- AJAX-based chat interface for real-time interaction

### `study_assistant/`

Django project configuration:

- Global settings and routing
- ASGI/WSGI entry points
- App integration and middleware

---

## How the System Works

1. User uploads a PDF document
2. Text is extracted and stored as a note
3. The document is chunked and embedded using Gemini embeddings
4. FAISS builds a vector index for semantic search
5. When a user asks a question:
   - Relevant chunks are retrieved via vector similarity
   - Recent chat history is appended as context
   - Gemini generates a grounded response
6. The conversation is stored and reused for future context

This creates a persistent, context-aware study assistant per document.

---

## Security & Environment

The system relies on environment-based configuration for API keys and secrets. Sensitive credentials are never hardcoded and are managed via environment variables and user profile settings.

---

## Author

**Vinay Kumar Sharma**

Django & AI-focused developer building real-world, production-style applications that combine backend engineering with modern LLM workflows.
