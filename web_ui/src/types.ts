export interface StrategyParameter {
    name: string
    label: string
    type: string
    default: any
    options?: string[]
}

export interface StrategyMetadata {
    id: string
    label: string
    description: string
    logic_explanation: string
    risk_profile: string
    parameters: StrategyParameter[]
}

export interface Signal {
    timestamp: string
    side: string
    price: number
    // Audit Fields
    trigger?: string
    amount?: number
    cost?: number
    commission?: number
    cash_before?: number
    cash_after?: number
    pos_before?: number
    pos_after?: number
    equity_after?: number
    signal_raw?: number
    indicators?: Record<string, number>
    rule?: string
}

export interface Regime {
    label: string
    total_return: number
    volatility: number
    sharpe: number
    percentage_of_time: number
}

export interface BacktestResult {
    total_return: number
    max_drawdown: number
    sharpe_ratio: number
    final_equity: number
    total_trades: number
    benchmark_return: number
    equity_curve: number[]
    benchmark_curve: number[]
    drawdown_curve: number[]
    signals: Signal[]
    regime_stats: Regime[]
    p_value: number
    is_significant: boolean
    stability_variance: number
    inaction_value: number
    research_conclusion: string
    stress_moment_explanation: string
    risk_assessment: string
    // New Metrics
    time_in_market_pct: number
    time_in_loss_pct: number
    max_latent_drawdown: number
    avg_trade_duration_candles: number
    max_money_at_risk: number
}

export interface Discovery {
    scenarios: any[]
    strategies: StrategyMetadata[]
    available_symbols: string[]
    available_timeframes: string[]
}
