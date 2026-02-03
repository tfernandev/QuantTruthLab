import pandas as pd
import numpy as np
from core.strategies.base import Strategy
from core.analysis.indicators import TechnicalAnalysis as TA

class RsiStrategy(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        length = int(self.params.get('length', 14))
        oversold = float(self.params.get('oversold', 30))
        overbought = float(self.params.get('overbought', 70))
        df = df.copy()
        TA.add_rsi(df, length=length)
        col_rsi = f"RSI_{length}"
        df['signal'] = 0
        # Valid signals: exit previous state and cross trigger
        buy_signal = (df[col_rsi] < oversold) & (df[col_rsi].shift(1) >= oversold)
        sell_signal = (df[col_rsi] > overbought) & (df[col_rsi].shift(1) <= overbought)
        df.loc[buy_signal, 'signal'] = 1
        df.loc[sell_signal, 'signal'] = -1
        return df
    
    def describe(self) -> str:
        return "Indicador de momentum que busca puntos de sobreextensión. Compra cuando el precio 'cae demasiado' y vende cuando 'sube demasiado'."

    def parameters_schema(self) -> list:
        return [
            {"name": "length", "label": "Periodo RSI", "type": "number", "default": 14},
            {"name": "oversold", "label": "Nivel Sobrevenda", "type": "number", "default": 30},
            {"name": "overbought", "label": "Nivel Sobrecompra", "type": "number", "default": 70}
        ]

class SmaCrossoverStrategy(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        fast = int(self.params.get('fast_period', 10))
        slow = int(self.params.get('slow_period', 20))
        df = df.copy()
        TA.add_sma(df, length=fast)
        TA.add_sma(df, length=slow)
        df['signal'] = 0
        buy = (df[f"SMA_{fast}"] > df[f"SMA_{slow}"]) & (df[f"SMA_{fast}"].shift(1) <= df[f"SMA_{slow}"].shift(1))
        sell = (df[f"SMA_{fast}"] < df[f"SMA_{slow}"]) & (df[f"SMA_{fast}"].shift(1) >= df[f"SMA_{slow}"].shift(1))
        df.loc[buy, 'signal'] = 1
        df.loc[sell, 'signal'] = -1
        return df

    def describe(self) -> str:
        return "Estrategia de seguimiento de tendencia. Busca capturar movimientos largos cuando una tendencia de corto plazo supera a la de largo plazo."

    def parameters_schema(self) -> list:
        return [
            {"name": "fast_period", "label": "Media Rápida", "type": "number", "default": 10},
            {"name": "slow_period", "label": "Media Lenta", "type": "number", "default": 20}
        ]

class VolatilityFilterStrategy(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        length = int(self.params.get('length', 20))
        threshold = float(self.params.get('threshold_pct', 0.5)) / 100
        df = df.copy()
        df['returns'] = df['close'].pct_change()
        df['vol'] = df['returns'].rolling(length).std()
        # 1 means "High Volatility / Trendable", 0 means "Low Volatility / Noise"
        df['signal'] = (df['vol'] > threshold).astype(int)
        return df

    def describe(self) -> str:
        return "Actúa como un 'interruptor' térmico. Detecta si el mercado tiene suficiente energía (volatilidad) para que las estrategias funcionen."

    def parameters_schema(self) -> list:
        return [
            {"name": "length", "label": "Ventana de Volatilidad", "type": "number", "default": 20},
            {"name": "threshold_pct", "label": "Umbral de Energía %", "type": "number", "default": 0.5}
        ]

class RandomStrategy(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        seed = int(self.params.get('seed', 42))
        prob = float(self.params.get('probability', 0.05))
        # Ensure probability is within [0, 1] for safety during stability audits
        prob = max(0.0, min(1.0, prob))
        
        np.random.seed(seed)
        df = df.copy()
        
        # We must ensure p sums to 1.0 exactly to avoid numpy errors
        p_none = 1.0 - prob
        p_buy = prob / 2.0
        p_sell = 1.0 - p_none - p_buy # Ensure exact sum to 1.0
        
        signals = np.random.choice([0, 1, -1], size=len(df), p=[p_none, p_buy, p_sell])
        df['signal'] = signals
        return df

    def describe(self) -> str:
        return "Baseline de control. Si tu estrategia no puede batir a este generador de números aleatorios, no tienes una ventaja real."

    def parameters_schema(self) -> list:
        return [
            {"name": "probability", "label": "Densidad de Señales", "type": "number", "default": 0.05},
            {"name": "seed", "label": "Semilla (Aleatoriedad)", "type": "number", "default": 42}
        ]

class EnsembleStrategy(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        strat_a_id = self.params.get('strat_a', 'SmaCrossover')
        strat_b_id = self.params.get('strat_b', 'VolatilityFilter')
        op = self.params.get('operator', 'FILTER')
        
        # Instantiate sub-strategies with their specific params if available
        s_a = StrategyFactory.get_strategy(strat_a_id, self.params.get('params_a', {}))
        s_b = StrategyFactory.get_strategy(strat_b_id, self.params.get('params_b', {}))
        
        df_a = s_a.generate_signals(df.copy())
        df_b = s_b.generate_signals(df.copy())
        
        df_res = df.copy()
        sig_a = df_a['signal']
        sig_b = df_b['signal']
        
        if op == 'AND':
            df_res['signal'] = ((sig_a == sig_b) & (sig_a != 0)).astype(int) * sig_a
        elif op == 'OR':
            df_res['signal'] = sig_a.where(sig_a != 0, sig_b)
        elif op == 'FILTER':
            # Signal B must be 1 (Active) for Signal A to pass
            df_res['signal'] = (sig_b == 1).astype(int) * sig_a
        return df_res

    def describe(self) -> str:
        return "El cerebro del laboratorio. Permite combinar dos lógicas para ver si la unión crea estabilidad o solo añade complejidad innecesaria."

    def parameters_schema(self) -> list:
        return [
            {"name": "strat_a", "label": "Estrategia Base", "type": "select", "options": ["SmaCrossover", "RsiStrategy", "RandomStrategy"]},
            {"name": "strat_b", "label": "Filtro de Régimen", "type": "select", "options": ["VolatilityFilter", "SmaCrossover", "RsiStrategy"]},
            {"name": "operator", "label": "Operador Lógico", "type": "select", "options": ["FILTER", "AND", "OR"]}
        ]

class BollingerBandsStrategy(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        length = int(self.params.get('length', 20))
        std = float(self.params.get('std_dev', 2.0))
        df = df.copy()
        TA.add_bbands(df, length=length, std=std)
        
        # Pandas TA names columns like: BBL_20_2.0, BBM_20_2.0, BBU_20_2.0
        # We need to handle potential float discrepancies in column naming if needed
        # But usually it's standard. Let's find columns dynamically or strictly construct name.
        col_lower = f"BBL_{length}_{std}"
        col_upper = f"BBU_{length}_{std}"
        
        # Fallback if typical naming fails (e.g. integer vs float string in col name)
        # But for now assume standard behavior.
        
        df['signal'] = 0
        
        # Mean Reversion Logic: 
        # Buy if Close < Lower Band (Oversold condition) -> Betting on return to mean
        # Sell if Close > Upper Band (Overbought condition)
        
        # Logic 1: Immediate Signal on State
        buy_condition = df['close'] < df[col_lower]
        sell_condition = df['close'] > df[col_upper]
        
        df.loc[buy_condition, 'signal'] = 1
        df.loc[sell_condition, 'signal'] = -1
        return df

    def describe(self) -> str:
        return "Clásica reversión a la media. Compra cuando el precio cae por debajo de la banda inferior (barato) y vende cuando rompe la superior (caro)."

    def parameters_schema(self) -> list:
        return [
            {"name": "length", "label": "Periodo", "type": "number", "default": 20},
            {"name": "std_dev", "label": "Desviación Std", "type": "number", "default": 2.0}
        ]

class MacdStrategy(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        fast = int(self.params.get('fast', 12))
        slow = int(self.params.get('slow', 26))
        signal_span = int(self.params.get('signal', 9))
        df = df.copy()
        TA.add_macd(df, fast=fast, slow=slow, signal=signal_span)
        
        # Columns: MACD_12_26_9, MACDh_12_26_9 (hist), MACDs_12_26_9 (signal)
        col_macd = f"MACD_{fast}_{slow}_{signal_span}"
        col_signal = f"MACDs_{fast}_{slow}_{signal_span}"
        
        df['signal'] = 0
        
        # Crossover Logic
        # Buy: MACD crosses above Signal
        buy_cross = (df[col_macd] > df[col_signal]) & (df[col_macd].shift(1) <= df[col_signal].shift(1))
        # Sell: MACD crosses below Signal
        sell_cross = (df[col_macd] < df[col_signal]) & (df[col_macd].shift(1) >= df[col_signal].shift(1))
        
        df.loc[buy_cross, 'signal'] = 1
        df.loc[sell_cross, 'signal'] = -1
        return df

    def describe(self) -> str:
        return "El rey de los osciladores de tendencia. Busca cruces de impulso (momentum) para identificar nuevos ciclos de mercado."

    def parameters_schema(self) -> list:
        return [
             {"name": "fast", "label": "EMA Rápida", "type": "number", "default": 12},
             {"name": "slow", "label": "EMA Lenta", "type": "number", "default": 26},
             {"name": "signal", "label": "Señal", "type": "number", "default": 9}
        ]

class StrategyFactory:
    _strategies = {}

    @classmethod
    def register(cls, name: str, strategy_class):
        cls._strategies[name] = strategy_class

    @classmethod
    def get_strategy(cls, name: str, params: dict = None) -> Strategy:
        strat_class = cls._strategies.get(name)
        if not strat_class:
            # Fallback to default
            strat_class = cls._strategies.get("SmaCrossover")
        return strat_class(name, params or {})

# Registration of the Research Arsenal
StrategyFactory.register("SmaCrossover", SmaCrossoverStrategy)
StrategyFactory.register("RsiStrategy", RsiStrategy)
StrategyFactory.register("RandomStrategy", RandomStrategy)
StrategyFactory.register("EnsembleStrategy", EnsembleStrategy)
StrategyFactory.register("VolatilityFilter", VolatilityFilterStrategy)
StrategyFactory.register("BollingerBands", BollingerBandsStrategy)
StrategyFactory.register("MacdStrategy", MacdStrategy)
StrategyFactory.register("Default", SmaCrossoverStrategy)
