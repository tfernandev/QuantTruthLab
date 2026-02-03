from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class StrategyParameter(BaseModel):
    name: str
    label: str
    type: str
    default: Any
    options: Optional[List[str]] = None

class StrategyMetadata(BaseModel):
    id: str
    label: str
    description: str
    logic_explanation: str
    risk_profile: str
    parameters: List[StrategyParameter]
    default_params: Dict[str, Any]

class MarketScenario(BaseModel):
    id: str
    label: str
    description: str
    start: str
    end: str

class DiscoveryResponse(BaseModel):
    scenarios: List[MarketScenario]
    strategies: List[StrategyMetadata]
    available_symbols: List[str]
    available_timeframes: List[str]

class SignalInfo(BaseModel):
    timestamp: str
    side: str
    price: float
    # Audit Fields
    trigger: str = "SIGNAL" # SIGNAL, STOP_LOSS, TAKE_PROFIT
    amount: float = 0.0
    cost: float = 0.0
    commission: float = 0.0
    cash_before: float = 0.0
    cash_after: float = 0.0
    pos_before: float = 0.0
    pos_after: float = 0.0
    equity_after: float = 0.0
    # Context
    signal_raw: Optional[int] = None
    indicators: Optional[Dict[str, float]] = None
    rule: Optional[str] = None

class RegimeStat(BaseModel):
    label: str
    total_return: float
    volatility: float
    sharpe: float
    percentage_of_time: float

class AuditReport(BaseModel):
    is_ordered: bool
    duplicates: int
    gaps: int
    biggest_gap: str

class BacktestRequest(BaseModel):
    symbol: str
    timeframe: str
    strategy_name: str
    params: Dict[str, Any]
    initial_capital: float = 10000.0
    scenario_id: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    
    # Risk Management (Truth-Preserving)
    tp_type: Optional[str] = None # "percent", "absolute", "none"
    tp_value: Optional[float] = None
    sl_type: Optional[str] = None # "percent", "absolute", "none"
    sl_value: Optional[float] = None

class BacktestResult(BaseModel):
    # Core Alpha
    total_return: float
    max_drawdown: float
    sharpe_ratio: float
    final_equity: float
    total_trades: int
    benchmark_return: float
    
    # Curves
    equity_curve: List[float]
    benchmark_curve: List[float]
    drawdown_curve: List[float]
    
    # Audit & Truth
    signals: List[SignalInfo]
    regime_stats: List[RegimeStat]
    audit: AuditReport
    p_value: float
    is_significant: bool
    stability_variance: float
    inaction_value: float
    monte_carlo_runs: List[float]
    
    # Narratives
    research_conclusion: str
    stress_moment_explanation: str
    summary_text: str
    risk_assessment: str

    # Advanced Risk Metrics
    time_in_market_pct: float = 0.0
    time_in_loss_pct: float = 0.0
    max_latent_drawdown: float = 0.0 # Drawdown no realizado
    avg_trade_duration_candles: float = 0.0
    realized_drawdown: float = 0.0 # From closed trades only
    max_money_at_risk: float = 0.0
