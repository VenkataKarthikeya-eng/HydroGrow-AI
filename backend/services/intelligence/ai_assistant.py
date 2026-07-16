"""
ai_assistant.py — HydroGrow AI Conversational Assistant Engine (Phase 7 Upgrade)

This module provides context-aware conversational answers to grower queries.
It matches grower intents against a hydroponic knowledge base, retrieves relevant
agronomic data using a local TF-IDF search index, resolves follow-up questions using
conversation memory, and formats responses in a structured professional template.
"""

import os
import json
import re
from backend.rag.retriever import retrieve


class HydroGrowAssistant:
    def __init__(self):
        # Resolve path to knowledge base
        base_dir = os.path.dirname(os.path.abspath(__file__))
        kb_path = os.path.normpath(os.path.join(base_dir, "..", "..", "..", "knowledge", "hydroponic_knowledge.json"))
        
        if os.path.exists(kb_path):
            with open(kb_path, "r", encoding="utf-8") as f:
                self.kb = json.load(f)
        else:
            raise FileNotFoundError(f"Hydroponic knowledge base not found at {kb_path}")

    def get_response(self, user_query: str, context: dict) -> str:
        """
        Analyze the user query, determine grower intent, retrieve relevant knowledge chunks,
        merge prediction context, and construct a professional formatted response.

        Parameters
        ----------
        user_query : str
            The question typed by the grower.
        context : dict
            Context containing:
            - user_inputs (dict)
            - prediction_result (dict)
            - recommendation_outputs (list)
            - explanation_output (dict)
            - conversation_history (list, optional)

        Returns
        -------
        str
            A structured, helpful markdown response.
        """
        query = user_query.lower().strip()
        if not query:
            return "Please type a question, and I will help you optimize your hydroponic lettuce grow-room!"

        # Extract context variables
        inputs = context.get("user_inputs", {})
        pred_res = context.get("prediction_result", {})
        recs = context.get("recommendation_outputs", [])
        explanation = context.get("explanation_output", {})
        history = context.get("conversation_history", [])

        # -------------------------------------------------------------------
        # PART 4 — AI Conversation Memory & Follow-up Resolution
        # -------------------------------------------------------------------
        resolved_query = query
        is_followup = False
        
        # Check if the query is a short follow-up or contains ambiguous terms
        ambiguous_keywords = ["it", "that", "this", "them", "fix", "solve", "why", "how", "adjust", "range", "value"]
        query_words = query.split()
        
        if history and (len(query_words) < 4 or any(w in ambiguous_keywords for w in query_words)):
            # Search for the previous user query in history
            # The current user query is already at history[-1], so check history[:-1]
            prev_user_query = None
            for msg in reversed(history[:-1]):
                if msg["role"] == "user":
                    prev_user_query = msg["content"].lower().strip()
                    break
            
            if prev_user_query:
                # Merge query with previous context for better intent matching
                resolved_query = f"{prev_user_query} {query}"
                is_followup = True

        # -------------------------------------------------------------------
        # PART 1 & 2 — Intent Detection & Retrieval
        # -------------------------------------------------------------------
        # Perform retrieval on the query
        retrieved_chunks = retrieve(user_query, top_k=3)

        # -------------------------------------------------------------------
        # INTENT 1: Specific parameters (pH, EC, CO2, Temp, Humidity, Water Temp)
        # -------------------------------------------------------------------
        param_mapping = {
            "ph": ("water_ph", "Water pH"),
            "ec": ("water_ec", "Water EC"),
            "electrical conductivity": ("water_ec", "Water EC"),
            "co2": ("co2", "CO2 Level"),
            "carbon dioxide": ("co2", "CO2 Level"),
            "humidity": ("humidity", "Humidity"),
            "rh": ("humidity", "Humidity"),
            "air temp": ("air_temperature", "Air Temperature"),
            "air temperature": ("air_temperature", "Air Temperature"),
            "water temp": ("water_temperature", "Water Temperature"),
            "water temperature": ("water_temperature", "Water Temperature"),
        }

        matched_param = None
        for keyword, (kb_key, param_display) in param_mapping.items():
            # Perform strict word boundary search
            if re.search(r'\b' + re.escape(keyword) + r'\b', resolved_query):
                matched_param = (kb_key, param_display)
                break

        if matched_param:
            kb_key, param_display = matched_param
            kb_data = self.kb["optimal_ranges"][kb_key]
            current_val = inputs.get(kb_key, "N/A")
            unit = kb_data.get("unit", "")
            formatted_val = f"{current_val} {unit}".strip() if current_val != "N/A" else "N/A"

            # Check status and action from recommendations
            status = "Optimal"
            action = "Maintain current levels."
            for r in recs:
                if r["parameter"] == param_display:
                    status = r["status"]
                    action = r["action"]
                    break

            opt_min = kb_data["min"]
            opt_max = kb_data["max"]
            
            followup_tag = " (Follow-up context applied)" if is_followup else ""

            return (
                f"### 📊 Parameter Insight: {param_display}{followup_tag}\n\n"
                f"🌱 **Analysis:**\n"
                f"Your active {param_display} is currently classified as **{status}**.\n\n"
                f"📊 **Evidence:**\n"
                f"- **Current Value:** `{formatted_val}` (Status: **{status}**)\n"
                f"- **Ideal Range:** {opt_min} - {opt_max} {unit}\n"
                f"- **Physiological Impact:** {kb_data['explanation']}\n\n"
                f"💡 **Recommendation:**\n"
                f"{action}"
            )

        # -------------------------------------------------------------------
        # INTENT 2: Common Diseases & Problems
        # -------------------------------------------------------------------
        matched_problem = None
        for problem in self.kb["common_problems"]:
            p_name = problem["name"]
            p_keywords = [p_name.lower()]
            if "pythium" in p_name.lower():
                p_keywords.append("pythium")
            if "root rot" in p_name.lower():
                p_keywords.append("root rot")
            if "tip burn" in p_name.lower():
                p_keywords.append("tipburn")

            # Check using word boundaries
            matched_by_word = False
            for kw in p_keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', resolved_query):
                    matched_by_word = True
                    break
            
            if matched_by_word:
                matched_problem = problem
                break

        if matched_problem:
            p_name = matched_problem["name"]
            followup_tag = " (Follow-up context applied)" if is_followup else ""
            return (
                f"### ⚠️ Agricultural Problem: {p_name}{followup_tag}\n\n"
                f"🌱 **Analysis:**\n"
                f"Primary Diagnosis: {p_name}. Cause: {matched_problem['cause']}\n\n"
                f"📊 **Evidence:**\n"
                f"- **Symptom:** {matched_problem['symptom']}\n"
                f"- **Retrieved RAG Support:** {retrieved_chunks[0]['content'] if retrieved_chunks else 'N/A'}\n\n"
                f"💡 **Recommendation:**\n"
                f"{matched_problem['solution']}"
            )

        # -------------------------------------------------------------------
        # INTENT 3: Growth Stages
        # -------------------------------------------------------------------
        stages_keywords = ["stage", "stages", "phase", "phases", "cycle", "cycles", "germination", "nursery", "vegetative", "harvest"]
        if re.search(r'\b(?:' + '|'.join(stages_keywords) + r')\b', resolved_query):
            response = "### 📅 Lettuce Growth Phases\n"
            response += "Hydroponic leaf lettuce grows through 4 key developmental phases:\n\n"
            for stage in self.kb["growth_stages"]:
                response += f"#### {stage['stage']} ({stage['duration']})\n"
                response += f"- **Target Conditions:** {stage['conditions']}\n\n"
            return response

        # -------------------------------------------------------------------
        # INTENT 4: Explain prediction details / why low / why high
        # -------------------------------------------------------------------
        prediction_keywords = ["why", "explain prediction", "only", "low", "predicted", "result", "weight", "prediction"]
        if re.search(r'\b(?:' + '|'.join(prediction_keywords) + r')\b', resolved_query):
            opps = explanation.get("improvement_opportunities", [])
            weight = pred_res.get("prediction_value", 0.0)
            category = pred_res.get("growth_category", "Poor")

            if opps:
                analysis = f"Your predicted fresh weight is **{weight:.1f} g** (classified as **{category}**)."
                
                evidence = ""
                recs_list = []
                for idx, opp in enumerate(opps, 1):
                    param_name = opp["factor"]
                    exp_text = opp["explanation"]
                    
                    # Find corresponding recommendation action
                    action_text = "Adjust setting."
                    for r in recs:
                        if r["parameter"] == param_name:
                            action_text = r["action"]
                            break
                    
                    evidence += f"- **{param_name}**: {exp_text}\n"
                    recs_list.append(f"{idx}. **{param_name}**: {action_text}")
                
                recommendations = "\n".join(recs_list)

                return (
                    f"### 🤖 Prediction Context Diagnostic\n\n"
                    f"🌱 **Analysis:**\n"
                    f"{analysis}\n\n"
                    f"📊 **Evidence:**\n"
                    f"{evidence}\n"
                    f"💡 **Recommendation:**\n"
                    f"{recommendations}"
                )
            else:
                return (
                    f"### 🤖 Prediction Context Diagnostic\n\n"
                    f"🌱 **Analysis:**\n"
                    f"Your predicted fresh weight is **{weight:.1f} g**, which is classified as **{category}**.\n\n"
                    f"📊 **Evidence:**\n"
                    f"All of your environmental and water parameters are within optimal ranges! Excellent management.\n\n"
                    f"💡 **Recommendation:**\n"
                    f"Maintain current levels. To push weight even higher, optimize nursery lighting to maximize seedling transplant weight."
                )

        # -------------------------------------------------------------------
        # INTENT 5: How to improve / optimize lettuce growth
        # -------------------------------------------------------------------
        optimize_keywords = ["improve", "increase", "grow", "better", "maximize", "optimize", "yield", "more weight"]
        if re.search(r'\b(?:' + '|'.join(optimize_keywords) + r')\b', resolved_query):
            opps = explanation.get("improvement_opportunities", [])
            
            # Group active issues into environmental, nutrient, and management categories
            env_issues = []
            nut_issues = []
            seedling_issues = []
            
            for opp in opps:
                param = opp["factor"]
                action_text = next((r["action"] for r in recs if r["parameter"] == param), "Adjust parameter.")
                item = f"- **{param}**: {action_text}"
                
                if param in ["Air Temperature", "Humidity", "CO2 Level"]:
                    env_issues.append(item)
                elif param in ["Water pH", "Water EC", "Water Temperature", "Nutrient Solution Added"]:
                    nut_issues.append(item)
                else:
                    seedling_issues.append(item)

            analysis = "Lettuce growth can be maximized by adjusting environmental, nutrient, and seedling parameters."
            
            evidence = ""
            if env_issues:
                evidence += "**Environmental Improvements:**\n" + "\n".join(env_issues) + "\n\n"
            if nut_issues:
                evidence += "**Water & Nutrient Improvements:**\n" + "\n".join(nut_issues) + "\n\n"
            if seedling_issues:
                evidence += "**Seedling & General Management:**\n" + "\n".join(seedling_issues) + "\n\n"
                
            if not evidence:
                evidence = "All parameters are optimal. No bottlenecks detected in current dashboard state."

            recommendations = "Ensure daily calibration of pH/EC meters. If CO2 levels are warning, improve ventilation."

            return (
                f"### 🌿 Growth Optimization Advice\n\n"
                f"🌱 **Analysis:**\n"
                f"{analysis}\n\n"
                f"📊 **Evidence:**\n"
                f"{evidence}\n"
                f"💡 **Recommendation:**\n"
                f"{recommendations}"
            )

        # -------------------------------------------------------------------
        # RAG GENERAL SEARCH / DEFICIENCIES / DO / LIGHTING / HARVESTING
        # -------------------------------------------------------------------
        # If we have relevant retrieved knowledge (score > 0.08), use it
        if retrieved_chunks and retrieved_chunks[0]["score"] > 0.08:
            top_chunk = retrieved_chunks[0]
            source_tag = top_chunk["source"]
            content = top_chunk["content"]
            
            # Derive analysis and recommendation from retrieved content
            analysis = f"Retrieved knowledge from source: `{source_tag}` relevant to your query."
            evidence = content
            
            # Formulate recommendation
            recommendation = "Adjust parameters matching the evidence. Consult the full cultivation logs if problems persist."
            if "deficiencies" in source_tag:
                recommendation = "Review reservoir balances and adjust nutrient concentration."
            elif "lighting" in source_tag:
                recommendation = "Optimize lamp height and photoperiod to match the DLI targets."
            elif "dissolved_oxygen" in source_tag:
                recommendation = "Verify aerators are operational and keep water temperature under 21°C."
            elif "harvesting" in source_tag:
                recommendation = "Execute the flushing protocol and pre-cool heads immediately."
            elif "mistakes" in source_tag:
                recommendation = "Avoid the documented mistake. Keep daily logs of pH, EC, and water temperatures."

            return (
                f"### 📖 Hydroponic Knowledge Finder\n\n"
                f"🌱 **Analysis:**\n"
                f"{analysis}\n\n"
                f"📊 **Evidence:**\n"
                f"{evidence}\n\n"
                f"💡 **Recommendation:**\n"
                f"{recommendation}"
            )

        # -------------------------------------------------------------------
        # FALLBACK: Helpful explanation helper
        # -------------------------------------------------------------------
        return (
            "I'm your **HydroGrow AI Assistant**. I can help you understand your lettuce fresh weight predictions, "
            "optimize hydroponic settings, manage nutrients, and troubleshoot common cultivation issues.\n\n"
            "Here are some examples of what you can ask me:\n"
            "- *'Why is my predicted growth low?'*\n"
            "- *'How can I improve my lettuce yield?'*\n"
            "- *'Explain what high water pH (7.2) does to lettuce.'*\n"
            "- *'How do I treat Pythium root rot?'*\n"
            "- *'What are the vegetative growth stages?'*\n\n"
            "Try asking one of the questions above!"
        )
