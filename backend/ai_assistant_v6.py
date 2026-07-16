"""
ai_assistant_v6.py — Backup of HydroGrow AI Conversational Assistant Engine (Phase 6)
"""

import os
import json


class HydroGrowAssistant:
    def __init__(self):
        # Resolve path to knowledge base
        base_dir = os.path.dirname(os.path.abspath(__file__))
        kb_path = os.path.normpath(os.path.join(base_dir, "..", "knowledge", "hydroponic_knowledge.json"))
        
        if os.path.exists(kb_path):
            with open(kb_path, "r", encoding="utf-8") as f:
                self.kb = json.load(f)
        else:
            raise FileNotFoundError(f"Hydroponic knowledge base not found at {kb_path}")

    def get_response(self, user_query: str, context: dict) -> str:
        query = user_query.lower().strip()
        if not query:
            return "Please type a question, and I will help you optimize your hydroponic lettuce grow-room!"

        inputs = context.get("user_inputs", {})
        pred_res = context.get("prediction_result", {})
        recs = context.get("recommendation_outputs", [])
        explanation = context.get("explanation_output", {})

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

        for keyword, (kb_key, param_display) in param_mapping.items():
            if keyword in query:
                kb_data = self.kb["optimal_ranges"][kb_key]
                current_val = inputs.get(kb_key, "N/A")
                unit = kb_data.get("unit", "")
                formatted_val = f"{current_val} {unit}".strip() if current_val != "N/A" else "N/A"

                status = "Optimal"
                action = "Maintain current levels."
                for r in recs:
                    if r["parameter"] == param_display:
                        status = r["status"]
                        action = r["action"]
                        break

                opt_min = kb_data["min"]
                opt_max = kb_data["max"]
                
                return (
                    f"### 📊 Parameter Insight: {param_display}\n"
                    f"- **Ideal Range:** {opt_min} - {opt_max} {unit}\n"
                    f"- **Current Value:** `{formatted_val}` (Status: **{status}**)\n\n"
                    f"**Physiological Influence:**\n"
                    f"{kb_data['explanation']}\n\n"
                    f"**Recommended Grower Action:**\n"
                    f"{action}"
                )

        for problem in self.kb["common_problems"]:
            p_name = problem["name"]
            p_keywords = [p_name.lower()]
            if "pythium" in p_name.lower():
                p_keywords.append("pythium")
            if "root rot" in p_name.lower():
                p_keywords.append("root rot")
            if "tip burn" in p_name.lower():
                p_keywords.append("tipburn")

            if any(kw in query for kw in p_keywords):
                return (
                    f"### ⚠️ Agricultural Problem: {p_name}\n"
                    f"- **Symptom:** {problem['symptom']}\n"
                    f"- **Primary Cause:** {problem['cause']}\n\n"
                    f"**Actionable Solution Plan:**\n"
                    f"{problem['solution']}"
                )

        if any(kw in query for kw in ["stage", "phase", "cycle", "germination", "nursery", "vegetative", "harvest"]):
            response = "### 📅 Lettuce Growth Phases\n"
            response += "Hydroponic leaf lettuce grows through 4 key developmental phases:\n\n"
            for stage in self.kb["growth_stages"]:
                response += f"#### {stage['stage']} ({stage['duration']})\n"
                response += f"- **Target Conditions:** {stage['conditions']}\n\n"
            return response

        if any(kw in query for kw in ["why", "explain prediction", "only", "low", "predicted", "result", "weight", "prediction"]):
            opps = explanation.get("improvement_opportunities", [])
            weight = pred_res.get("prediction_value", 0.0)
            category = pred_res.get("growth_category", "Poor")

            if opps:
                response = (
                    f"Your predicted fresh weight of **{weight:.1f} g** (classified as **{category}**) "
                    "is influenced by the following sub-optimal parameters in your setup:\n\n"
                )
                for idx, opp in enumerate(opps, 1):
                    param_name = opp["factor"]
                    exp_text = opp["explanation"]
                    
                    action_text = "Adjust setting."
                    for r in recs:
                        if r["parameter"] == param_name:
                            action_text = r["action"]
                            break
                    
                    response += f"{idx}. **{param_name}**:\n"
                    response += f"   *Physiological Impact:* {exp_text}\n"
                    response += f"   *Grower Action:* {action_text}\n\n"
                
                response += "Addressing these bottlenecks will improve your predicted crop yield."
                return response
            else:
                return (
                    f"Your predicted fresh weight is **{weight:.1f} g**, which is classified as **{category}**.\n\n"
                    "All of your environmental and water parameters are within optimal ranges! Excellent management. "
                    "The model's weight estimate is based on the combination of these optimal parameters "
                    "and your seedling starting conditions. To push the weight even higher, consider optimizing nursery lighting "
                    "to maximize starting transplant weight."
                )

        if any(kw in query for kw in ["improve", "increase", "grow", "better", "maximize", "optimize", "yield", "more weight"]):
            opps = explanation.get("improvement_opportunities", [])
            response = "### 🌿 Growth Optimization Advice\n\n"
            
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

            response += "#### 🌡️ Environmental Improvements\n"
            if env_issues:
                response += "\n".join(env_issues) + "\n\n"
            else:
                response += "- Air temperature, humidity, and CO2 are in optimal ranges. Maintain current settings.\n\n"

            response += "#### 💧 Water & Nutrient Improvements\n"
            if nut_issues:
                response += "\n".join(nut_issues) + "\n\n"
            else:
                response += "- Water pH, EC, temperature, and feeding rates are optimal. Keep reservoir topped up.\n\n"

            response += "#### ⚙️ Seedling & General Management\n"
            if seedling_issues:
                response += "\n".join(seedling_issues) + "\n\n"
            else:
                response += "- Starting seedling conditions are within standard dimensions. Transplant with care.\n\n"
                
            return response

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
