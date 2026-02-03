from datetime import datetime, timezone

MARKET_SCENARIOS = [
    {
        "id": "bull_2021",
        "label": "El Gran Bull Run (2021)",
        "description": "Un periodo de euforia masiva donde los precios subieron verticalmente. Ideal para probar estrategias de tendencia.",
        "start": "2021-01-01T00:00:00Z",
        "end": "2021-12-31T23:59:59Z",
        "tags": ["Tendencia", "Optimismo", "Alta Rentabilidad"]
    },
    {
        "id": "bear_2022",
        "label": "Invierno Cripto (2022)",
        "description": "Periodo de caídas constantes y mercado bajista agresivo. Pone a prueba la gestión de riesgo y la capacidad de proteger capital.",
        "start": "2022-01-01T00:00:00Z",
        "end": "2022-12-31T23:59:59Z",
        "tags": ["Caída", "Riesgo", "Estrés"]
    },
    {
        "id": "recovery_2023",
        "label": "Recuperación y Calma (2023)",
        "description": "El mercado sale del abismo y comienza a consolidar. Mezcla de periodos laterales con subidas moderadas.",
        "start": "2023-01-01T00:00:00Z",
        "end": "2023-12-31T23:59:59Z",
        "tags": ["Lado", "Recuperación", "Consolidación"]
    },
    {
        "id": "etf_2024",
        "label": "Era Institucional (2024-Presente)",
        "description": "Entrada de los ETFs y adopción institucional. Mayor madurez del mercado y volatilidad profesional.",
        "start": "2024-01-01T00:00:00Z",
        "end": "2025-01-01T00:00:00Z", # Adjusted to current
        "tags": ["Madurez", "Institucional", "Volatilidad"]
    }
]

STRATEGY_METADATA = {
    "SmaCrossover": {
        "label": "Cruce de Medias (Trend Following)",
        "description": "Una de las estrategias más clásicas. Intenta capturar grandes tendencias comprando cuando el impulso de corto plazo supera al de largo plazo. Es lenta pero segura en mercados alcistas claros.",
        "logic_explanation": "Compra cuando la media de 20 periodos (rápida) cruza por encima de la de 50 (lenta). Vende cuando ocurre lo contrario.",
        "risk_profile": "Medio. Su mayor riesgo es el 'whipsaw' (falsas señales) en mercados laterales.",
        "default_params": {"fast_period": 20, "slow_period": 50}
    },
    "RsiStrategy": {
        "label": "Reversión a la Media (RSI Overbought/Oversold)",
        "description": "Basada en el impulso. Busca identificar cuando un activo ha subido demasiado rápido para vender, o bajado demasiado rápido para comprar.",
        "logic_explanation": "Compra cuando el RSI baja de 30 (sobreventa) y vende cuando supera 70 (sobrecompra).",
        "risk_profile": "Alto. Ir contra la tendencia puede ser peligroso si el mercado no retrocede.",
        "default_params": {"length": 14, "oversold": 30, "overbought": 70}
    },
    "RandomStrategy": {
        "label": "Baseline Azar (Random signals)",
        "description": "Genera señales aleatorias para validación estadística.",
        "logic_explanation": "Genera señales de compra/venta al azar con una frecuencia configurable.",
        "risk_profile": "Extremo. No tiene lógica de mercado.",
        "default_params": {"probability": 0.05, "seed": 42}
    },
    "VolatilityFilter": {
        "label": "Filtro de Régimen (Volatilidad)",
        "description": "Filtro que detecta periodos de mercado operable vs ruido.",
        "logic_explanation": "Marca periodos de alta volatilidad (operables) vs baja (laterales) para filtrar otras estrategias.",
        "risk_profile": "Defensivo. Busca evitar periodos de 'whipsaw'.",
        "default_params": {"threshold_pct": 0.5, "length": 20}
    },
    "EnsembleStrategy": {
        "label": "Combinador Lógico (AND/OR/FILTER)",
        "description": "Une dos lógicas para crear sistemas híbridos.",
        "logic_explanation": "Permite, por ejemplo, operar un SMA solo si el Filtro de Volatilidad está activo.",
        "risk_profile": "Variable. Depende de la combinación elegida.",
        "default_params": {"strat_a": "SmaCrossover", "strat_b": "VolatilityFilter", "operator": "FILTER"}
    }
}
