# Quant Terminal Research Platform v2.0

Esta plataforma es un entorno integral de investigación y simulación cuantitativa diseñado para explorar la historia de los mercados cripto sin necesidad de conocimientos previos de trading.

## Componentes Técnicos
1.  **Core (Engine)**: Motor en Python que gestiona la simulación de brokers, comisiones reales y lógica algorítmica.
2.  **Data Layer**: Persistencia en formato **Apache Parquet**, permitiendo simulaciones ultra-rápidas con años de historia local.
3.  **API (FastAPI)**: Orquestador que expone metadatos de estrategias y escenarios de mercado.
4.  **Terminal UI (React)**: Interfaz de grado profesional con visualización de riesgos y explicaciones en lenguaje natural.

## Cómo Iniciar la Plataforma

### 1. Iniciar el Motor Backend
Asegúrate de tener el entorno virtual activo y las dependencias instaladas.
```powershell
# Desde la raíz del proyecto
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --port 8000
```

### 2. Iniciar la Terminal Web
```powershell
# En una nueva terminal, entra en la carpeta web_ui
cd web_ui
npm run dev
```

## Guía de Exploración
1.  **Selecciona un Período**: Elige entre escenarios prediseñados como el "Invierno Cripto de 2022" o el "Bull Run de 2021".
2.  **Elige una Estrategia**: Lee la descripción educativa para entender qué intenta capturar el algoritmo.
3.  **Analiza los Resultados**:
    *   **Equity Curve**: La línea verde muestra cómo hubiera evolucionado tu dinero.
    *   **Evaluación de Riesgo**: Lee las advertencias automáticas sobre la volatilidad y pérdidas máximas (Drawdown).
    *   **Métricas Explicadas**: Pasa el ratón o lee los pies de página de cada tarjeta para entender qué significa el Sharpe Ratio y otros indicadores técnicos.

---
*Aviso: Este sistema es puramente educativo y de simulación. No opera con dinero real ni garantiza rentabilidades futuras.*
