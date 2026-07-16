"""
chat_interface.py — HydroGrow AI Dashboard Conversational Chat Interface

This module provides the Streamlit-based chat interface component, allowing growers
to ask questions about predictions, optimal parameter metrics, and troubleshooting solutions.
"""

import streamlit as st
from backend.services.intelligence.ai_assistant import HydroGrowAssistant


def trigger_rerun():
    """Safe wrapper for Streamlit rerun across different versions."""
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()


def render_chat_interface(user_inputs: dict, prediction_result: dict, recommendation_outputs: list, explanation_output: dict):
    """
    Render the Conversational AI Assistant component inside the Streamlit dashboard.

    Parameters
    ----------
    user_inputs : dict
        Grower inputs.
    prediction_result : dict
        Validated prediction details.
    recommendation_outputs : list
        Agricultural recommendations list.
    explanation_output : dict
        Prediction explanations.
    """
    # 1. Initialize chat session state
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # 2. Header and control buttons
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

    # 3. Display message log
    chat_container = st.container()
    with chat_container:
        if not st.session_state["chat_history"]:
            # Display greeting message when chat is empty
            with st.chat_message("assistant"):
                st.markdown(
                    "Hello! I am your **HydroGrow AI Assistant**. I have loaded your current dashboard "
                    "prediction context. You can ask me questions about your predicted lettuce weight, "
                    "nutrient solutions, optimal environmental parameters, or troubleshooting growing problems."
                )
        else:
            # Render all messages from history
            for msg in st.session_state["chat_history"]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

    # 4. Suggested Questions (shown when chat history is empty)
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

    # 5. Capture user inputs
    user_query = st.chat_input("Type your question here...")
    
    # Check if a suggested question button was clicked
    if "clicked_suggested_query" in st.session_state:
        user_query = st.session_state.pop("clicked_suggested_query")

    if user_query:
        # Append user message to history
        st.session_state["chat_history"].append({"role": "user", "content": user_query})
        
        # Prepare context payload
        context = {
            "user_inputs": user_inputs,
            "prediction_result": prediction_result,
            "recommendation_outputs": recommendation_outputs,
            "explanation_output": explanation_output,
            "conversation_history": st.session_state["chat_history"]
        }
        
        # Generate answer using assistant engine
        try:
            assistant = HydroGrowAssistant()
            response = assistant.get_response(user_query, context)
        except Exception as e:
            response = f"Sorry, I encountered an error while processing your request: {str(e)}"

        # Append assistant answer to history
        st.session_state["chat_history"].append({"role": "assistant", "content": response})
        
        # Trigger page rerun to show updated chat messages
        trigger_rerun()
