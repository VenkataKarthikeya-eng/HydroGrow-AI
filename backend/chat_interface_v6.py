"""
chat_interface_v6.py — Backup of HydroGrow AI Dashboard Conversational Chat Interface (Phase 6)
"""

import streamlit as st
from backend.ai_assistant_v6 import HydroGrowAssistant


def trigger_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()


def render_chat_interface(user_inputs: dict, prediction_result: dict, recommendation_outputs: list, explanation_output: dict):
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    st.markdown("### 💬 Ask HydroGrow AI Assistant")
    
    col_desc, col_clear = st.columns([5, 1.2])
    with col_desc:
        st.caption(
            "Ask questions about your growth prediction results, environmental parameters, "
            "nutrient guidelines, or troubleshoot diseases (e.g. root rot, tip burn)."
        )
    with col_clear:
        if st.button("🗑️ Clear Chat", key="clear_chat_button", use_container_width=True):
            st.session_state["chat_history"] = []
            trigger_rerun()

    st.markdown("---")

    chat_container = st.container()
    with chat_container:
        if not st.session_state["chat_history"]:
            with st.chat_message("assistant"):
                st.markdown(
                    "Hello! I am your **HydroGrow AI Assistant**. I have loaded your current dashboard "
                    "prediction context. You can ask me questions about your predicted lettuce weight, "
                    "nutrient solutions, optimal environmental parameters, or troubleshooting growing problems."
                )
        else:
            for msg in st.session_state["chat_history"]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

    if not st.session_state["chat_history"]:
        st.markdown("<small>💡 Suggested questions for this prediction:</small>", unsafe_allow_html=True)
        s_col1, s_col2, s_col3 = st.columns(3)
        
        with s_col1:
            if st.button("Why is my prediction low?", key="s_low_q_btn", use_container_width=True):
                st.session_state["clicked_suggested_query"] = "Why is my predicted growth low?"
                trigger_rerun()
        with s_col2:
            if st.button("How can I improve my yield?", key="s_imp_q_btn", use_container_width=True):
                st.session_state["clicked_suggested_query"] = "How can I improve my lettuce growth?"
                trigger_rerun()
        with s_col3:
            if st.button("How to treat root rot?", key="s_rot_q_btn", use_container_width=True):
                st.session_state["clicked_suggested_query"] = "How do I solve root rot (Pythium)?"
                trigger_rerun()

    user_query = st.chat_input("Type your question here...")
    
    if "clicked_suggested_query" in st.session_state:
        user_query = st.session_state.pop("clicked_suggested_query")

    if user_query:
        st.session_state["chat_history"].append({"role": "user", "content": user_query})
        
        context = {
            "user_inputs": user_inputs,
            "prediction_result": prediction_result,
            "recommendation_outputs": recommendation_outputs,
            "explanation_output": explanation_output
        }
        
        try:
            assistant = HydroGrowAssistant()
            response = assistant.get_response(user_query, context)
        except Exception as e:
            response = f"Sorry, I encountered an error while processing your request: {str(e)}"

        st.session_state["chat_history"].append({"role": "assistant", "content": response})
        trigger_rerun()
