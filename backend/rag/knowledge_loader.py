"""
knowledge_loader.py — RAG Document Loader for HydroGrow AI

Loads the hydroponic knowledge base JSON and flattens it into individual,
searchable documents with clear source tags.
"""

import os
import json


def load_knowledge_base() -> list[dict]:
    """
    Loads hydroponic_knowledge.json and yields flattened document records.
    Each record is a dictionary: {"content": str, "source": str}
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    kb_path = os.path.normpath(os.path.join(base_dir, "..", "..", "knowledge", "hydroponic_knowledge.json"))
    
    if not os.path.exists(kb_path):
        raise FileNotFoundError(f"Knowledge base file not found at {kb_path}")
        
    with open(kb_path, "r", encoding="utf-8") as f:
        kb = json.load(f)
        
    documents = []

    # 1. Optimal Ranges
    for key, data in kb.get("optimal_ranges", {}).items():
        unit = data.get("unit", "")
        unit_str = f" in {unit}" if unit else ""
        content = (
            f"Optimal range for {key.replace('_', ' ')}: "
            f"minimum {data['min']}, maximum {data['max']}{unit_str}. "
            f"Explanation: {data['explanation']}"
        )
        documents.append({
            "content": content,
            "source": f"optimal_ranges/{key}"
        })

    # 2. Nutrient Guidelines
    for key, val in kb.get("nutrient_guidelines", {}).items():
        content = f"Nutrient guidelines for {key}: {val}"
        documents.append({
            "content": content,
            "source": f"nutrient_guidelines/{key}"
        })

    # 3. Common Problems
    for problem in kb.get("common_problems", []):
        name = problem["name"]
        content = (
            f"Problem: {name}. "
            f"Symptom: {problem['symptom']} "
            f"Primary Cause: {problem['cause']} "
            f"Actionable Solution Plan: {problem['solution']}"
        )
        documents.append({
            "content": content,
            "source": f"common_problems/{name}"
        })

    # 4. Growth Stages
    for stage in kb.get("growth_stages", []):
        name = stage["stage"]
        content = (
            f"Lettuce growth stage: {name}. "
            f"Duration: {stage['duration']}. "
            f"Target Conditions: {stage['conditions']}"
        )
        documents.append({
            "content": content,
            "source": f"growth_stages/{name}"
        })

    # 5. Nutrient Deficiencies
    for defic in kb.get("nutrient_deficiencies", []):
        element = defic["element"]
        content = (
            f"Nutrient deficiency: {element} deficiency. "
            f"Symptoms: {defic['symptoms']} "
            f"Primary Causes: {defic['causes']} "
            f"Actionable Corrections: {defic['corrections']}"
        )
        documents.append({
            "content": content,
            "source": f"nutrient_deficiencies/{element}"
        })

    # 6. Root Diseases
    for disease in kb.get("root_diseases", []):
        name = disease["disease"]
        content = (
            f"Root disease: {name}. "
            f"Symptoms: {disease['symptoms']} "
            f"Primary Causes: {disease['causes']} "
            f"Actionable Corrections: {disease['corrections']}"
        )
        documents.append({
            "content": content,
            "source": f"root_diseases/{name}"
        })

    # 7. Lighting Requirements
    for key, val in kb.get("lighting_requirements", {}).items():
        content = f"Lighting requirements - {key.replace('_', ' ')}: {val}"
        documents.append({
            "content": content,
            "source": f"lighting_requirements/{key}"
        })

    # 8. Dissolved Oxygen Management
    for key, val in kb.get("dissolved_oxygen_management", {}).items():
        content = f"Dissolved oxygen management - {key.replace('_', ' ')}: {val}"
        documents.append({
            "content": content,
            "source": f"dissolved_oxygen_management/{key}"
        })

    # 9. Harvesting Optimization
    for key, val in kb.get("harvesting_optimization", {}).items():
        content = f"Harvesting optimization - {key.replace('_', ' ')}: {val}"
        documents.append({
            "content": content,
            "source": f"harvesting_optimization/{key}"
        })

    # 10. Greenhouse Mistakes
    for mistake in kb.get("greenhouse_mistakes", []):
        name = mistake["mistake"]
        content = (
            f"Common greenhouse mistake: {name}. "
            f"Consequence: {mistake['consequence']} "
            f"Prevention: {mistake['prevention']}"
        )
        documents.append({
            "content": content,
            "source": f"greenhouse_mistakes/{name}"
        })

    return documents


if __name__ == "__main__":
    docs = load_knowledge_base()
    print(f"Loaded {len(docs)} documents successfully.")
    for d in docs[:3]:
        print(f"\n- Source: {d['source']}\n  Content: {d['content']}")
