# Quant Terminal: Research & Simulation Platform
**Estado del Proyecto: v2.5 (Análisis Forense y Comparativo)**

Esta plataforma es un entorno de simulación profesional diseñado para democratizar el análisis cuantitativo y la educación financiera en el espacio cripto.

## 🏗️ Arquitectura Técnica
1.  **Data Persistence Layer (Parquet)**:
    *   Almacenamiento de alta performance basado en columnas.
    *   Dataset local: **BTC/USDT** y **ETH/USDT** con velas de 1h desde Ener-2021 hasta Ene-2025.
    *   Simulaciones instantáneas sin API externa durante el proceso de backtest.

2.  **Core Engine (Python)**:
    *   **SimulatedBroker**: Motor de ejecución que replica comisiones reales (0.1%), slippage y gestión de caja/cripto.
    *   **Strategy Analysis**: Generación de señales basada en indicadores vectorizados (SMA Crossovers, etc).
    *   **PerformanceMetrics**: Cálculo dinámico de Sharpe Ratio, Max Drawdown y Benchmark Alpha.

3.  **Intelligent Backend (FastAPI)**:
    *   **Discovery API**: Expone automáticamente escenarios históricos y estrategias disponibles.
    *   **Simulación Narrativa**: Traduce resultados numéricos a conclusiones pedagógicas.

4.  **Terminal UI (React/Vite/Tailwind)**:
    *   Diseño inspirado en terminales financieras tipo Bloomberg.
    *   **Gráfica Dual**: Comparativa visual entre la estrategia seleccionada y el mercado (Buy & Hold).

## 🎓 Funcionalidades Educativas (Nivel Terminal)
-   **Análisis Forense (Stress Analysis)**: Identifica por qué ocurrió la mayor caída del capital (¿Culpa del mercado o error del algoritmo?).
-   **Métrica de Valor (Alpha)**: Separa el rendimiento obtenido por la "suerte" del mercado del rendimiento generado por la "habilidad" de la estrategia.
-   **Escenarios Narrativos**: Reemplaza las fechas técnicas por contextos históricos reales (Bull Run 2021, Crypto Winter 2022, etc.).

## 📊 Integridad de Datos
-   **Dataset Validado**: Los datos locales coinciden con el histórico de Binance promediando los precios de cierre por hora.
-   **Simulación Conservadora**: Las comisiones reducen la ganancia bruta para evitar el sesgo de optimismo ("papel aguanta todo").

---
*Este sistema no opera con dinero real y es puramente educativo.*
