import pandas as pd
try:
    import pandas_ta as ta
    print("pandas_ta imported")
except ImportError as e:
    print(f"Error importing pandas_ta: {e}")

df = pd.DataFrame({'close': [1, 2, 3, 4, 5]*10})
print("DF created")
try:
    df.ta.sma(length=2, append=True)
    print("SMA calculated")
    print(df.head())
except Exception as e:
    print(f"Error calculating SMA: {e}")
