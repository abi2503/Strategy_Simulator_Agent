# streamlit_app.py
import sys
import os
sys.path.append(os.path.abspath("src"))

import streamlit as st
import pandas as pd
from src.rag_store import StrategyStore
from src.rag_query import StrategyRetriever
from src.llm_explainer import explain_strategy_with_llm
from src.strategy_loader import load_strategy_excel

st.set_page_config(page_title="Strategy Insight Agent", layout="centered")
st.title("📈 LLM-Powered Strategy Explainer")

st.markdown("Upload a strategy summary or Excel file to get AI-driven explanations and comparisons.")

# Sidebar: Upload Excel file
tab1, tab2 = st.tabs(["📄 Manual Summary", "📤 Upload Excel"])

with tab2:
    uploaded_file = st.file_uploader("Upload strategy Excel (.xlsx)", type=["xlsx"])
    auto_summary = ""
    if uploaded_file:
        try:
            df = load_strategy_excel(uploaded_file)
            start = df['Date'].min().strftime('%Y-%m')
            end = df['Date'].max().strftime('%Y-%m')
            alpha_ret = df['Alpha_Cum'].iloc[-1]
            hedge_ret = df['Hedge_Cum'].iloc[-1]
            combined_ret = df['Combined_Cum'].iloc[-1]

            auto_summary = f"""
            This strategy contains monthly returns from an Alpha model and a Hedge strategy.
            The combined return each period is calculated as: Alpha + Hedge.

            Performance summary:
            - Start Date: {start}
            - End Date: {end}
            - Final Cumulative Alpha Return: {alpha_ret:.2%}
            - Final Cumulative Hedge Return: {hedge_ret:.2%}
            - Final Combined Strategy Return: {combined_ret:.2%}
            """
            st.success("✅ Summary generated from Excel!")

            # Optional save to memory
            save = st.checkbox("💾 Save this strategy to memory")
            if save:
                store = StrategyStore()
                metadata = {
                    "strategy_name": uploaded_file.name,
                    "file": uploaded_file.name,
                    "period": f"{start} to {end}",
                    "final_alpha_return": float(alpha_ret),
                    "final_hedge_return": float(hedge_ret),
                    "final_combined_return": float(combined_ret)
                }
                store.add_strategy(auto_summary, metadata)
                store.save()
                st.success("🧠 Strategy embedded into RAG memory!")

        except Exception as e:
            st.error(f"Failed to load strategy: {e}")

# Tab 1: Manual text area
with tab1:
    strategy_text = st.text_area("✍️ Paste your strategy summary below:", value=auto_summary, height=250)
    top_k = st.slider("🔍 Number of similar strategies to retrieve:", 1, 5, 1)

    if st.button("🔎 Analyze Strategy") and strategy_text:
        with st.spinner("Retrieving similar strategies and generating explanation..."):
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            retriever = StrategyRetriever(
                index_path=os.path.join(BASE_DIR, 'faiss_index.index'),
                meta_path=os.path.join(BASE_DIR, 'strategy_metadata.pkl')
            )
            results = retriever.query(strategy_text, top_k=top_k)

            context = ""
            for i, match in enumerate(results):
                meta = match['metadata']
                context += f"\n\n---\nTop {i+1} Match:\n- Name: {meta['strategy_name']}\n- Period: {meta['period']}\n- Final Return: {meta['final_combined_return']:.2%}"

            prompt = f"""
            Strategy Summary:
            {strategy_text}

            Context from similar strategies:
            {context}

            Please explain the above strategy and compare it to the retrieved ones. Discuss:
            - Structure and intention
            - Performance vs similar strategies
            - Risk factors or enhancements
            """

            explanation = explain_strategy_with_llm(prompt)

        st.subheader("🧠 Strategy Explanation")
        st.write(explanation)
