# seed_rag.py
"""
This script initializes the FAISS index by embedding and storing a sample strategy.
Run this once before using the retriever.
"""
from src.rag_store import StrategyStore

store = StrategyStore()

summary_text = """
This strategy contains monthly returns from an Alpha model and a Hedge strategy.
The combined return each period is calculated as: Alpha + Hedge.

Performance summary:
- Start Date: 2009-10
- End Date: 2019-11
- Final Cumulative Alpha Return: 58.41%
- Final Cumulative Hedge Return: -13.06%
- Final Combined Strategy Return: 39.47%
"""

metadata = {
    "strategy_name": "Alpha + Hedge",
    "file": "alpha_strategy_plus_hedge_assignment_exercise.xlsx",
    "period": "2009-10 to 2019-11",
    "final_alpha_return": 0.5841,
    "final_hedge_return": -0.1306,
    "final_combined_return": 0.3947
}

store.add_strategy(summary_text, metadata)
store.save()
print("✅ Strategy stored and FAISS index initialized.")
