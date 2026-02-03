# Reporte de Investigación Cuantitativa: Validación de Edge
**Investigador**: Antigravity (Quant Research Unit)
**Fecha**: 15 de Enero, 2026

## 1. Resumen de Hallazgos
Tras realizar una auditoría estadística rigurosa, la conclusión es clara: **Las estrategias actuales (SMA Crossover y RSI) no demuestran un edge estadísticamente significativo sobre el azar en los escenarios analizados.**

## 2. Benchmark contra el Azar (Random Baseline)
Se implementó una `RandomStrategy` que genera señales aleatorias con la misma frecuencia que los algoritmos testeados.

| Escenario | SMA Return | RSI Return | Random Return | Conclusión |
| :--- | :--- | :--- | :--- | :--- |
| **Bull Run 2021** | -15.68% | -17.93% | -16.59% | Indistinguible |
| **ETF 2024** | -17.44% | +0.64% | +18.31% | El azar superó al SMA |

*Nota: Los rendimientos negativos en mercados alcistas se deben a la ejecución T+1 y al impacto de las comisiones (0.1% por trade), que erosionan el capital en estrategias de alta frecuencia.*

## 3. Validación Estadística (T-Test)
Se compararon las distribuciones de retornos diarios de SMA contra la `RandomStrategy` en el periodo 2024.
- **P-Value**: **0.4829**
- **Interpretación**: No se puede rechazar la Hipótesis Nula (H0). Existe un 48% de probabilidad de que los resultados de la estrategia se deban puramente al azar. Para considerar un "edge", necesitaríamos un p-value < 0.05.

## 4. Análisis de Sensibilidad (Overfitting Check)
Se variaron los parámetros de las medias móviles (10/20, 20/50, 50/200).
- **Resultado**: Los cambios en el rendimiento son erráticos. Una estrategia robusta debería mostrar una degradación suave; aquí vemos colapsos de rentabilidad ante cambios mínimos, lo que sugiere que cualquier resultado positivo previo era producto de la suerte o del *lookahead bias* (ya corregido).

## 5. Diagnóstico de Falta de Edge
¿Por qué las estrategias "fallan"?
1. **Fricción (Comisiones)**: En temporalidades de 1h, el ruido del mercado genera muchas señales falsas. El costo de 0.1% por operación mata la rentabilidad.
2. **Latencia de Señal (T+1)**: Al eliminar el *lookahead bias*, el bot entra un periodo más tarde. En cripto, un periodo de 1h puede significar perder gran parte del movimiento.
3. **Falta de Filtro de Régimen**: Las estrategias operan igual en mercados laterales que en tendencia, siendo "aserradas" (whipsawed) constantemente.

## 6. Líneas de Investigación para el "Edge Real"
Para encontrar valor explotable, se propone:
- **Filtros de Volatilidad**: No operar si el ATR es demasiado bajo (mercado lateral).
- **Confirmación de Tendencia**: Usar una media de mayor jerarquía (ej. 200 periodos) como filtro de dirección.
- **Optimización de Ejecución**: En lugar de órdenes Market a ciegas, usar lógica de entrada basada en niveles de soporte/resistencia.

---
**Veredicto Final**: El sistema es técnicamente perfecto y honesto, pero las estrategias actuales son puramente educativas y no poseen valor predictivo superior a lanzar una moneda.
