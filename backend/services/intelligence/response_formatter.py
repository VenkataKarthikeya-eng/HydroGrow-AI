class ResponseFormatter:
    """
    Formats agricultural diagnostic responses in standard Markdown templates
    specifying analysis, evidence, and actions.
    """
    @staticmethod
    def format_parameter_insight(
        param_display: str,
        status: str,
        formatted_val: str,
        opt_min: float,
        opt_max: float,
        unit: str,
        explanation: str,
        action: str,
        is_followup: bool = False
    ) -> str:
        followup_tag = " (Follow-up context applied)" if is_followup else ""
        return (
            f"### 📊 Parameter Insight: {param_display}{followup_tag}\n\n"
            f"🌱 **Analysis:**\n"
            f"Your active {param_display} is currently classified as **{status}**.\n\n"
            f"📊 **Evidence:**\n"
            f"- **Current Value:** `{formatted_val}` (Status: **{status}**)\n"
            f"- **Ideal Range:** {opt_min} - {opt_max} {unit}\n"
            f"- **Physiological Impact:** {explanation}\n\n"
            f"💡 **Recommendation:**\n"
            f"{action}"
        )

    @staticmethod
    def format_disease_diagnosis(
        disease_name: str,
        cause: str,
        symptom: str,
        solution: str,
        rag_snippet: str,
        is_followup: bool = False
    ) -> str:
        followup_tag = " (Follow-up context applied)" if is_followup else ""
        return (
            f"### ⚠️ Agricultural Problem: {disease_name}{followup_tag}\n\n"
            f"🌱 **Analysis:**\n"
            f"Primary Diagnosis: {disease_name}. Cause: {cause}\n\n"
            f"📊 **Evidence:**\n"
            f"- **Symptom:** {symptom}\n"
            f"- **Retrieved RAG Support:** {rag_snippet}\n\n"
            f"💡 **Recommendation:**\n"
            f"{solution}"
        )

    @staticmethod
    def format_prediction_diagnostic(
        predicted_weight: float,
        growth_category: str,
        evidence: str,
        recommendations: str
    ) -> str:
        return (
            f"### 🤖 Prediction Context Diagnostic\n\n"
            f"🌱 **Analysis:**\n"
            f"Your predicted fresh weight is **{predicted_weight:.1f} g** (classified as **{growth_category}**).\n\n"
            f"📊 **Evidence:**\n"
            f"{evidence}\n"
            f"💡 **Recommendation:**\n"
            f"{recommendations}"
        )

    @staticmethod
    def format_growth_optimization(
        analysis: str,
        evidence: str,
        recommendations: str
    ) -> str:
        return (
            f"### 🌿 Growth Optimization Advice\n\n"
            f"🌱 **Analysis:**\n"
            f"{analysis}\n\n"
            f"📊 **Evidence:**\n"
            f"{evidence}\n"
            f"💡 **Recommendation:**\n"
            f"{recommendations}"
        )

    @staticmethod
    def format_general_response(
        title: str,
        analysis: str,
        evidence: str,
        recommendations: str
    ) -> str:
        return (
            f"### {title}\n\n"
            f"🌱 **Analysis:**\n"
            f"{analysis}\n\n"
            f"📊 **Evidence:**\n"
            f"{evidence}\n\n"
            f"💡 **Recommendation:**\n"
            f"{recommendations}"
        )
