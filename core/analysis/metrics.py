import pandas as pd
import numpy as np
from typing import Dict

class PerformanceMetrics:
    @staticmethod
    def calculate(equity_curve: pd.Series, price_series: pd.Series = None) -> Dict[str, float]:
        """
        Calculates key metrics. 
        If price_series is provided, calculates benchmark (Buy & Hold) for comparison.
        """
        if equity_curve.empty:
            return {}

        returns = equity_curve.pct_change().dropna()
        
        # Total Return
        start_equity = equity_curve.iloc[0]
        end_equity = equity_curve.iloc[-1]
        total_return_pct = (end_equity - start_equity) / start_equity * 100
        
        # Max Drawdown
        rolling_max = equity_curve.cummax()
        drawdown = (equity_curve - rolling_max) / rolling_max
        max_drawdown_pct = drawdown.min() * 100
        
        # Benchmark Return
        benchmark_return_pct = 0.0
        if price_series is not None and not price_series.empty:
            p_start = price_series.iloc[0]
            p_end = price_series.iloc[-1]
            benchmark_return_pct = (p_end - p_start) / p_start * 100

        # Sharpe Ratio
        mean_return = returns.mean()
        std_return = returns.std()
        if returns.empty or std_return == 0 or np.isnan(std_return):
            sharpe = 0
        else:
            sharpe = (mean_return / std_return) * np.sqrt(8760)

        res = {
            "Total Return %": total_return_pct,
            "Max Drawdown %": max_drawdown_pct,
            "Sharpe Ratio": sharpe,
            "Final Equity": end_equity,
            "Benchmark Return %": benchmark_return_pct
        }
        
        # Sanitize for JSON (replace NaN/Inf with 0)
        for k, v in res.items():
            if np.isnan(v) or np.isinf(v):
                res[k] = 0.0
            else:
                res[k] = round(float(v), 2)
                
        return res
