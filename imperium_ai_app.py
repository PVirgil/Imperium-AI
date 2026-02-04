# imperium_ai_app.py

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq
import logging

# Setup
logging.basicConfig(level=logging.INFO)
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Core Agent Call

def call_agent(prompt: str, model="mixtral-8x7b-32768") -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are Imperium AI, an enterprise-grade AI designed to manage legal, financial, and operational intelligence for global asset managers."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Agents

def legal_ops_agent(context: str, doc_type: str) -> str:
    prompt = f"Generate a professional {doc_type} for a global fund given this context: {context}"
    return call_agent(prompt)

def cfo_ops_agent(df: pd.DataFrame) -> str:
    prompt = f"Based on this capital data: {df.head(3).to_dict()}, summarize cash positions, outstanding capital calls, and recommend treasury strategy."
    return call_agent(prompt)

def investor_comms_agent(question: str, context: str) -> str:
    prompt = f"An LP asks: {question}\nFund context: {context}\nWrite a clear, compliant answer as an IR professional."
    return call_agent(prompt)

def esg_intel_agent(context: str) -> str:
    prompt = f"Analyze this fund's ESG performance: {context}\nReport EU/US scores and improvement steps."
    return call_agent(prompt)

def risk_strategy_agent(df: pd.DataFrame) -> str:
    prompt = f"Given fund performance data: {df.head(3).to_dict()}, analyze risk exposures and suggest rebalancing."
    return call_agent(prompt)

# UI

def main():
    st.set_page_config("Imperium AI – Institutional Core", page_icon="🏛", layout="wide")
    st.title("🏛 Imperium AI")
    st.markdown("Enterprise AI system for managing legal, ops, LPs, ESG and fund strategy across global asset firms.")

    uploaded_file = st.file_uploader("Upload fund data (CSV)", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Data uploaded successfully.")
    else:
        df = pd.DataFrame()

    tabs = st.tabs([
        "📄 Legal Ops",
        "💰 CFO Ops",
        "💬 Investor Comms",
        "🌿 ESG Intelligence",
        "📊 Risk Strategy"
    ])

    with tabs[0]:
        st.subheader("📄 Legal Automation")
        doc_type = st.selectbox("Choose document", ["NDA", "LPA", "Side Letter", "Board Resolution"])
        context = st.text_area("Enter fund/legal context")
        if st.button("Generate Legal Doc"):
            if context:
                result = legal_ops_agent(context, doc_type)
                st.text_area("Legal Draft", result, height=400)
            else:
                st.error("Please enter context.")

    with tabs[1]:
        st.subheader("💰 Treasury & CFO Dashboard")
        if st.button("Run CFO Ops"):
            if df.empty:
                st.error("Upload fund data.")
            else:
                result = cfo_ops_agent(df)
                st.text_area("CFO Summary", result, height=400)

    with tabs[2]:
        st.subheader("💬 LP Communications")
        context = st.text_area("Enter LP context (fund strategy, update)")
        question = st.text_input("LP Question")
        if st.button("Generate Response"):
            if context and question:
                result = investor_comms_agent(question, context)
                st.text_area("LP Response", result, height=300)
            else:
                st.error("Provide context and question.")

    with tabs[3]:
        st.subheader("🌿 ESG Intel")
        context = st.text_area("Describe ESG policy or impact")
        if st.button("Run ESG Analysis"):
            if context:
                result = esg_intel_agent(context)
                st.text_area("ESG Report", result, height=400)
            else:
                st.error("Please enter ESG context.")

    with tabs[4]:
        st.subheader("📊 Risk & Strategy Analysis")
        if st.button("Analyze Risk"):
            if df.empty:
                st.error("Upload fund return data.")
            else:
                result = risk_strategy_agent(df)
                st.text_area("Risk Report", result, height=400)

if __name__ == "__main__":
    main()
