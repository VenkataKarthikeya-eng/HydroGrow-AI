# Phase 2 Technical Report: HydroGrow AI Professional React Frontend

This report documents the design, architecture, and implementation details of the HydroGrow AI Professional React Frontend (Phase 2), replacing the pre-existing monolithic Streamlit interface with a production-grade Single Page Application (SPA).

---

## 1. Architectural Comparison

### Pre-existing Monolithic Streamlit Architecture
Previously, the Streamlit interface (`backend/app.py`) loaded the python files directly, coupling visual components and logic.

```
+-------------------------------------------------------------+
|               Streamlit Front-End Dashboard                 |
+-------------------------------------+-----------------------+
                                      |
                                      v (Direct Python Imports)
+-------------------------------------------------------------+
|                     Intelligence Services                   |
|  (predict, recommendations, explanation, retriever, index)  |
+-------------------------------------------------------------+
```

### New Decoupled React + FastAPI Client-Server Architecture
The React SPA runs in a separate process, interacting exclusively with the FastAPI router using asynchronous JSON payloads. The pre-existing Streamlit interface is preserved in place as a working backup.

```
+-----------------------------------+     +-----------------------------------+
|     React Single Page App         |     |       Streamlit Dashboard         |
|     (Vite + Tailwind Client)      |     |         (Working Backup)          |
+-----------------+-----------------+     +-----------------+-----------------+
                  | (Axios REST JSON)                       | (Direct Python)
                  v                                         v
+-----------------+-----------------------------------------+-----------------+
|                       FastAPI API Backend Router                            |
|                          (backend/api/main.py)                              |
+-----------------------------------+-----------------------------------------+
                                    |
                                    v (Internal Service Bindings)
+-----------------------------------+-----------------------------------------+
|                         Intelligence Layer Services                         |
|   (prediction, recommendation_engine, explanation_engine, retriever, RAG)   |
+-----------------------------------------------------------------------------+
```

---

## 2. Directory Structure

The new frontend project files are contained within `frontend/` directory, maintaining clean separation from python services and data stores.

```
frontend/
├── .env
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── index.html
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── index.css
    ├── api/
    │   ├── client.js
    │   ├── predictionApi.js
    │   └── assistantApi.js
    ├── context/
    │   └── AppContext.jsx
    ├── components/
    │   ├── Navbar.jsx
    │   ├── Footer.jsx
    │   ├── PredictionCard.jsx
    │   ├── MetricCard.jsx
    │   ├── RecommendationCard.jsx
    │   ├── ChatMessage.jsx
    │   └── LoadingSpinner.jsx
    └── pages/
        ├── LandingPage.jsx
        ├── PredictionDashboard.jsx
        └── AIAssistantPage.jsx
```

---

## 3. Component & State Design

### UI Components Listing
- **`Navbar.jsx`:** Premium responsive navigation bar featuring Sprout logo and session grower indicators.
- **`Footer.jsx`:** Subtle footer with copyrights and system help guides.
- **`MetricCard.jsx`:** Informational widgets representing greenhouse settings summaries.
- **`PredictionCard.jsx`:** Highlights predicted fresh weight (g) inside a circular progress gauge (0 to 420g range) alongside growth category badges (Excellent/Good/Average/Poor) and biological validation status.
- **`RecommendationCard.jsx`:** Dynamic diagnostic cards highlighting parameter alerts (Optimal/Warning/Critical) and actionable steps.
- **`ChatMessage.jsx`:** Renders chatbot conversations, displaying Markdown structure, code highlighting, and expandable drawers showing reference sources retrieved from RAG indexing.
- **`LoadingSpinner.jsx`:** Animated foliage ring spinner showcasing background API activities.

### Context State & Context Sharing (`AppContext.jsx`)
React Context manages prediction inputs, calculated weights, and chat logs. To provide advanced diagnostic capabilities:
1. When a user runs a prediction, results (explanation, recommendations, categories) are saved in Context state.
2. When the user opens the AI Assistant, the current dashboard context is automatically attached to the payload sent to `POST /api/chat`:
```javascript
{
  "message": "Why is my yield low?",
  "conversation_history": [...],
  "context": {
    "user_inputs": { ... },
    "prediction_result": { "prediction_value": 245.5, "growth_category": "Poor" },
    "recommendation_outputs": [ ... ],
    "explanation_output": { ... }
  }
}
```
This enables the chatbot to provide context-aware feedback (e.g., "Your pH is critically low at 4.5, which is causing your prediction to decrease...").

### LocalStorage Persistence
Both conversation logs (`hydrogrow_chat_history`) and prediction inputs/results (`hydrogrow_inputs`, `hydrogrow_prediction`) are synced to `localStorage`. This prevents session data loss upon page reloads.

---

## 4. API Integration Details

### Central Client Configuration
Axios utilizes a localized config consuming Vite environment variables.
- **File:** `frontend/.env`
  ```env
  VITE_API_BASE_URL=http://localhost:8000
  ```
- **File:** `frontend/src/api/client.js`
  ```javascript
  import axios from 'axios';
  const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
  const client = axios.create({
    baseURL,
    headers: { 'Content-Type': 'application/json' },
    timeout: 30000
  });
  export default client;
  ```

### API Handlers
- **`predictionApi.js`:** `predictGrowth(params)` mapped to `POST /api/predict`. Handles connection timeouts and formats invalid input exceptions.
- **`assistantApi.js`:** `sendMessage(message, history, context)` mapped to `POST /api/chat`. Handles system offline cases and intent fallback results.

---

## 5. Offline Markdown Processor
To display structured AI responses cleanly, `ChatMessage.jsx` parses common Markdown elements without external libraries:
- **Headings:** `#`, `##`, `###` headings render as formatted title elements.
- **Lists:** `-` or `*` or numeric lists render as list items.
- **Formatting:** `**bold**` text and `` `inline code` `` tags are highlighted.
- **Code Blocks:** Fenced triple backticks (`` ``` ``) render inside monospace code blocks.

---

## 6. Verification and Builds

### Backend Testing Suite
All backend prediction modules, validation engines, and intelligence interfaces were verified with the python test suite:
```powershell
python -m unittest discover -s tests
```
**Results:**
```
Ran 35 tests in 0.120s

OK
```

### Production Frontend Compilation
The React client build was compiled using Vite's roll-up pipeline:
```powershell
cd frontend
npm run build
```
**Results:**
```
vite v5.4.21 building for production...
✓ 1463 modules transformed.
rendering chunks...
dist/index.html                   1.16 kB │ gzip:  0.64 kB
dist/assets/index-BkNVz1iQ.css   29.68 kB │ gzip:  5.82 kB
dist/assets/index-92OUyEAe.js   266.44 kB │ gzip: 82.83 kB
✓ built in 5.11s
```
Build completed with zero errors and warnings.

---

## 7. Developer Operations Guide

### Starting the API Server
Start the FastAPI server on port 8000:
```powershell
python -m uvicorn backend.api.main:app --port 8000 --reload
```

### Starting the React Development Client
Start the Vite developer build on port 3000:
```powershell
cd frontend
npm run dev
```
Open `http://localhost:3000` in the browser to access the dashboard.
