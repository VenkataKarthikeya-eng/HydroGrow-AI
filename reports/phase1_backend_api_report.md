# Phase 1 Technical Report: HydroGrow AI Backend API Layer

This report documents the architectural upgrade of the HydroGrow AI platform through the introduction of a FastAPI backend API layer. The backend API layer wraps existing Machine Learning (ML) prediction capabilities and conversational Retrieval-Augmented Generation (RAG) assistant features as clean, production-ready RESTful endpoints.

---

## 1. System Architecture Evolution

### Previous Architecture (Monolithic Streamlit Dashboard)
Previously, the Streamlit dashboard (`backend/app.py`) was responsible for both rendering the user interface and direct execution of business/intelligence logic. This tight coupling made it difficult to integrate external applications (e.g., custom frontend frameworks, mobile applications) or scale individual service modules.

```
+-------------------------------------------------------------+
|               Streamlit Front-End Dashboard                 |
+-------------------------------------+-----------------------+
                                      |
                                      v (Direct Imports)
+-------------------------------------------------------------+
|                      Intelligence Layer                      |
|                                                             |
|  +------------------+  +-----------------+  +------------+  |
|  |  prediction.py   |  | recommendations |  | assistant  |  |
|  +--------+---------+  +-----------------+  +-----+------+  |
|           |                                       |         |
|           v                                       v         |
|  +--------+---------+                       +-----+------+  |
|  |   validation.py  |                       |  RAG (rag/*|  |
|  +------------------+                       +------------+  |
+-------------------------------------------------------------+
```

### New API-Augmented Architecture (Service-Oriented Wrapper)
The FastAPI backend acts as an intermediate wrapper layer, exposing standard REST endpoints without altering the underlying core business, ML prediction, or RAG intelligence files. The Streamlit dashboard continues to run alongside, importing the exact same services, while external systems can access everything via JSON.

```
+----------------------------------+   +----------------------------------+
|    Streamlit UI (Dashboard)      |   |  Future React Web App / Clients  |
+----------------+-----------------+   +----------------+-----------------+
                 | (Direct Python)                      | (JSON REST API)
                 |                                      v
                 |                            +---------------------------+
                 |                            |    FastAPI Routing Layer  |
                 |                            |   (backend/api/main.py)   |
                 |                            +---------+-----------------+
                 |                                      |
                 +-----------------+--------------------+
                                   |
                                   v
+----------------------------------+--------------------------------------+
|                           Service Layer                                 |
|                                                                         |
|  +--------------------------------+   +------------------------------+  |
|  |       Prediction Service       |   |      Intelligence Service    |  |
|  |     (prediction_routes.py)     |   |      (assistant_routes.py)   |  |
|  |                                |   |                              |  |
|  |  +--------------------------+  |   |  +------------------------+  |  |
|  |  |      prediction.py       |  |   |  |    ai_assistant.py     |  |  |
|  |  +------------+-------------+  |   |  +-----------+------------+  |  |
|  |               |                |   |              |                |  |
|  |  +------------v-------------+  |   |  +-----------v------------+  |  |
|  |  |  prediction_validation   |  |   |  |   rag/retriever.py     |  |  |
|  |  +--------------------------+  |   |  +------------------------+  |  |
|  +--------------------------------+   +------------------------------+  |
+-------------------------------------------------------------------------+
```

---

## 2. API Endpoints Documentation

### 2.1 Health Check
- **Endpoint**: `GET /health`
- **Description**: Returns basic operational metrics and confirmation that the API service is active.
- **Request Example**:
  ```http
  GET /health HTTP/1.1
  Host: localhost:8000
  ```
- **Response Payload (JSON)**:
  ```json
  {
      "status": "running",
      "service": "HydroGrow AI API",
      "version": "1.0.0"
  }
  ```

### 2.2 Crop Prediction Pipeline
- **Endpoint**: `POST /api/predict`
- **Description**: Receives 11 parameters from the grow room, dynamically computes derived features at the boundary, executes prediction, runs agricultural recommendations rules, and returns explainable AI diagnostics.
- **Request Example**:
  ```json
  {
      "air_temperature": 22.0,
      "humidity": 60.0,
      "co2": 450.0,
      "water_ph": 6.2,
      "water_ec": 2.0,
      "water_temperature": 23.0,
      "nutrient_solution": 400.0,
      "water_consumption": 170.0,
      "seedling_height": 12.0,
      "seedling_weight": 4.0,
      "root_length": 7.0
  }
  ```
- **Response Payload (JSON)**:
  ```json
  {
      "prediction": {
          "predicted_weight": 189.38,
          "growth_category": "⚠️ Poor"
      },
      "validation": {
          "prediction_value": 189.38,
          "original_prediction": 189.38,
          "was_adjusted": false,
          "validation_message": "Prediction is within training bounds."
      },
      "recommendations": [
          {
              "type": "success",
              "parameter": "Water pH",
              "value": "6.2",
              "status": "Optimal",
              "message": "Water pH is within the ideal lettuce growth range...",
              "action": "Maintain current pH level and continue daily monitoring."
          }
      ],
      "explanation": {
          "summary": "HydroGrow AI predicts 189.4g fresh weight. The crop performance is classified as Poor based on training distribution.",
          "positive_factors": [
              {
                  "factor": "Water pH",
                  "explanation": "Water pH (6.2) is optimal and supports nutrient absorption."
              }
          ],
          "improvement_opportunities": [],
          "confidence_explanation": "Model predictions represent expected harvest weight..."
      },
      "metadata": {
          "derived_inputs": {
              "water_tds": 1.0,
              "acid_consumption_ml": 40.0
          }
      }
  }
  ```

### 2.3 Conversational AI Assistant
- **Endpoint**: `POST /api/chat`
- **Description**: Integrates conversational memory, intent detection, and a local RAG document index to generate formatted grower answers.
- **Request Example**:
  ```json
  {
      "message": "Why is my prediction only 245g?",
      "conversation_history": [
          {"role": "user", "content": "How can I improve my lettuce yield?"},
          {"role": "assistant", "content": "Keep water pH optimal (5.5-6.5)..."}
      ],
      "context": {
          "user_inputs": {
              "water_ph": 4.5,
              "water_ec": 2.0,
              "water_tds": 1.0,
              "water_temperature": 21.0,
              "air_temperature": 22.0,
              "humidity": 60.0,
              "co2": 350.0,
              "nutrient_solution_ml": 400.0,
              "water_consumption_l": 170.0,
              "acid_consumption_ml": 40.0,
              "initial_height_cm": 12.0,
              "initial_weight_g": 4.0,
              "initial_root_length_cm": 7.0
          },
          "prediction_result": {
              "prediction_value": 245.5,
              "growth_category": "Poor"
          },
          "recommendation_outputs": [],
          "explanation_output": {
              "improvement_opportunities": [
                  {"factor": "Water pH", "explanation": "Water pH is critically low."}
              ]
          }
      }
  }
  ```
- **Response Payload (JSON)**:
  ```json
  {
      "response": "### 🤖 Prediction Context Diagnostic\n\n🌱 **Analysis:**\nYour predicted fresh weight is **245.5 g**...",
      "sources": ["calcium_deficiency_details", "water_ph_impacts"],
      "intent": "prediction_diagnostic"
  }
  ```

---

## 3. Testing and Verification Results

The API layer functionality was verified by writing unit and integration tests using FastAPI's `TestClient` class inside `tests/test_api.py`.

### Execution
We ran the full test suite encompassing 30 pre-existing tests and 5 new API-specific checks:
```powershell
python -m unittest discover -s tests
```

### Result Summary
```
Ran 35 tests in 0.105s

OK
```
All pre-existing crop calculations, validation boundaries, and conversational agent memory tests continue to pass alongside the new API endpoints.

---

## 4. Future React Frontend Integration Plan

Implementing the FastAPI layer enables a clean transition to a modern React dashboard. The integration process is structured as follows:

```
+-----------------------------------------------------------+
|                      React Frontend                       |
|  (State hooks: useQuery, useMutation, Axios, Context API) |
+-----------------------------+-----------------------------+
                              | (HTTP request payload)
                              v
+-----------------------------+-----------------------------+
|                 FastAPI CORS Middleware Layer             |
|   (Validates Origin header, authorizes HTTP verbs)       |
+-----------------------------+-----------------------------+
                              | (Deserialized models)
                              v
+-----------------------------+-----------------------------+
|                FastAPI Endpoints & Routers                |
+-----------------------------------------------------------+
```

### Implementation Checklist
1. **API Client Setup**: Install `axios` or configure native `fetch` wrappers inside the React project. Create API hook queries matching the FastAPI request Pydantic models.
2. **Context Provider**: Maintain context state representing current sliders/starting parameters values in React, sharing state among parameters input screens, prediction gauge cards, and chat assistant components.
3. **Cross-Origin Security (CORS)**: FastAPI `main.py` is configured with `CORSMiddleware` using `allow_origins=["*"]`. For production settings, this will be restricted to the verified React domain (e.g. `https://hydrogrow.ai`).
4. **Error Boundaries**: Leverage React Error Boundaries to catch fetch anomalies and render beautiful, human-readable notices reflecting `{ "error": true, "message": "...", "details": "..." }` responses.
