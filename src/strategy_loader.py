# src/strategy_loader.py
import pandas as pd

def load_strategy_excel(file_path: str, sheet_name: str = 'data') -> pd.DataFrame:
    """
    Load and clean Alpha + Hedge strategy Excel file.
    Returns a DataFrame with Date, Alpha, Hedge, and combined returns.
    """
    df_raw = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=2)
    df_raw.columns = ['Date', 'Alpha', 'Hedge'] + [f'Unused_{i}' for i in range(len(df_raw.columns) - 3)]
    df = df_raw[['Date', 'Alpha', 'Hedge']].dropna(subset=['Date', 'Alpha'])

    df['Date'] = pd.to_datetime(df['Date'])
    df['Alpha'] = pd.to_numeric(df['Alpha'], errors='coerce')
    df['Hedge'] = pd.to_numeric(df['Hedge'], errors='coerce')
    df = df.dropna()

    df['Alpha_Cum'] = (1 + df['Alpha']).cumprod() - 1
    df['Hedge_Cum'] = (1 + df['Hedge']).cumprod() - 1
    df['Combined_Cum'] = (1 + df['Alpha'] + df['Hedge']).cumprod() - 1
    return df

# src/returns_plotter.py
import matplotlib.pyplot as plt

def plot_cumulative_returns(df):
    """Plot cumulative returns of Alpha, Hedge, and Combined strategy."""
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
