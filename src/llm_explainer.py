# src/llm_explainer.py
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def explain_strategy_with_llm(strategy_text: str, model="gpt-4") -> str:
    prompt = f"""
    You are a financial quant expert. Explain the following strategy in simple, intuitive language:

    {strategy_text}

    Include:
    - What the Alpha and Hedge are doing
    - Why we combine them
    - What the performance means
    - Any risks or suggestions for improvement
    """

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert financial strategist and quant analyst."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=500,
    )

    return response.choices[0].message['content']
