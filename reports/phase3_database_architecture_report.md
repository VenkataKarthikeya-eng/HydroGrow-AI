# HydroGrow AI Phase 3: Database & Persistence Layer Architecture Report

## Overview
Phase 3 transitions HydroGrow AI from a stateless, session-dependent application to a production-grade enterprise platform. It integrates a relational database persistence layer, a JWT-based user authentication system, and a dynamic historical database mapping mechanism.

---

## 1. Database Schema Design
A multi-table PostgreSQL relational schema has been implemented inside `backend/database/models.py`:

```
   +------------------+
   |      users       |
   +------------------+
   | id (PK)          |<-------+
   | username (UQ)    |        |
   | email (UQ)       |        |
   | password_hash    |        |
   | created_at       |        |
   +------------------+        |
            |                  |
            | 1:N              | 1:N
            v                  |
   +------------------+        |
   |   predictions    |        |
   +------------------+        |
   | id (PK)          |        |
   | user_id (FK)     |        |
   | crop_type        |        |
   | input_parameters |        |
   | predicted_weight |        |
   | growth_category  |        |
   | recommendations  |        |
   | explanation      |        |
   | created_at       |        |
   +------------------+        |
                               |
   +------------------+        |
   |  conversations   |        |
   +------------------+        |
   | id (PK)          |<-------+
   | user_id (FK)     |
   | title            |
   | created_at       |
   +------------------+
            |
            | 1:N
            v
   +------------------+
   |     messages     |
   +------------------+
   | id (PK)          |
   | conversation_FK  |
   | role             |
   | content          |
   | sources          |
   | created_at       |
   +------------------+
```

### Table Definitions & Cascading Actions
- **`users`**: Stores unique username, unique email address, and hashed credentials.
- **`predictions`**: Persists parameters and biological inference details. If a user account is deleted, all historical prediction logs are cascaded (`ondelete="CASCADE"`).
- **`conversations`**: Captures message threads/sessions. Deleted users cascade conversation removals.
- **`messages`**: Contains user inquiries and AI diagnostics. Deleting a conversation thread cascades all nested message records.

---

## 2. Dynamic Database Connections & Environment Isolation
To decouple testing and local configurations, connections are managed inside `backend/database/connection.py`:
- **Development environment**: Connects to the local PostgreSQL database service running under `scram-sha-256` or `trust` authentication methods on port `5432`.
- **Test environment**: Automatically detects if the execution is running under python unit test suites (`"unittest" in sys.modules`). If true, it isolates data within a temporary file-based SQLite database (`test_hydrogrow.db`) which supports cross-session visibility while remaining isolated from PostgreSQL records.

Credentials are kept out of source files and are configured via a root `.env` file (backed by `.env.example`).

---

## 3. JWT-Based Security System
Implemented under `backend/authentication/`:
- **Bcrypt encryption**: Hashing and verification operations use direct `bcrypt` salting to ensure compatibility with Python 3.14.
- **Access tokens**: Standard HS256-signed JWT tokens containing username and ID details.
- **Dependencies injection**: 
  - `get_current_user` enforces 401 exceptions on protected endpoints.
  - `get_optional_current_user` extracts profile state if present, but falls back gracefully to stateless executions for anonymous requests (preserving Streamlit backup compatibility).

---

## 4. Frontend Integration Layout
Axios authorization interceptors in `frontend/src/api/client.js` append JWT Bearer headers dynamically from `localStorage`.
- **Split layouts**: Logged-in growers access sidebar memory threads (`ConversationList`) in `AIAssistantPage.jsx`.
- **Portal state**: Navbar adjusts dynamically to display user cards (`UserMenu` dropdown) or "Grower Portal" links.
- **Reload options**: Historical dashboard inputs are loaded back into current state on demand via `PredictionHistoryCard`.

---

## 5. Migrations & Automated Deployments
Alembic migrations are configured using the target metadata parameters.
- **Startup Auto-sync**: `models.Base.metadata.create_all(bind=engine)` runs on application startup inside `backend/api/main.py` to guarantee tables exist before requests arrive.
