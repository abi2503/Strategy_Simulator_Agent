# src/returns_plotter.py

import matplotlib.pyplot as plt

def plot_cumulative_returns(df):
    """
    Plot cumulative returns of Alpha, Hedge, and Combined strategy.

    Parameters:
    df (pd.DataFrame): DataFrame with Date, Alpha_Cum, Hedge_Cum, Combined_Cum columns
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Alpha_Cum'], label='Alpha Only', linewidth=2)
    plt.plot(df['Date'], df['Hedge_Cum'], label='Hedge Only', linestyle='--')
    plt.plot(df['Date'], df['Combined_Cum'], label='Alpha + Hedge', linewidth=2, color='black')

    plt.title('Cumulative Returns: Alpha vs. Hedge vs. Combined')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
