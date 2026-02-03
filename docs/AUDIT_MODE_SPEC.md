# Especificación: Modo Auditoría — "¿Cómo sé que los resultados son reales?"

## Objetivo

Dar al usuario **evidencia verificable** de que la simulación es honesta. Que pueda reproducir manualmente unas cuantas operaciones y comprobar que el equity final cuadra con las matemáticas.

---

## 1. Decisión por decisión: por qué se tomó cada acción

### Datos a exponer por cada trade

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **timestamp** | Momento exacto (UTC) | `2022-05-19 14:00:00` |
| **trigger** | Qué provocó la acción | `SEÑAL_ESTRATEGIA`, `STOP_LOSS`, `TAKE_PROFIT` |
| **side** | BUY / SELL | `BUY` |
| **precio_ejecucion** | Precio al que se ejecutó | `29234.50` |
| **cantidad** | Unidades del activo | `0.342` |
| **coste_total** | cantidad × precio | `9997.00` |
| **comision** | Fee aplicado (0.1%) | `9.997` |
| **saldo_cash_antes** | Cash antes del trade | `10000.00` |
| **saldo_cash_despues** | Cash después del trade | `0.00` |
| **posicion_antes** | Amount en cripto antes | `0` |
| **posicion_despues** | Amount en cripto después | `0.342` |
| **equity_despues** | cash + (posicion × precio) | `9997.00` |

### Contexto de la decisión (solo para SEÑAL_ESTRATEGIA)

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **senal_raw** | Valor de la señal | `1` (compra), `-1` (venta) |
| **indicadores_en_t** | Valores que generaron la señal | `SMA_20: 29100, SMA_50: 28900` |
| **vela_t** | OHLCV de la vela que disparó la señal | `open: 29100, high: 29300, low: 29000, close: 29234` |
| **regla_aplicada** | Descripción legible | "SMA_20 cruzó por encima de SMA_50" |

### UI propuesta

- **Lista expandible** de trades: al hacer clic en un trade se muestra el "por qué".
- **Filtros**: por tipo (señal / TP / SL), por rango de fechas.
- **Búsqueda por timestamp** para localizar operaciones concretas.

---

## 2. Exportar para revisión manual (CSV / JSON)

### 2.1 CSV de Trades

```csv
#,timestamp,trigger,side,precio,cantidad,coste,comision,cash_antes,cash_despues,pos_antes,pos_despues,equity_despues
1,2022-05-19 14:00:00,SEÑAL_ESTRATEGIA,BUY,29234.50,0.342,9997.00,9.997,10000.00,0.00,0,0.342,9997.00
2,2022-05-20 08:00:00,SEÑAL_ESTRATEGIA,SELL,28500.00,0.342,9747.00,9.747,0.00,9737.25,0.342,0,9737.25
```

- Nombre sugerido: `backtest_trades_{estrategia}_{symbol}_{fecha}.csv`
- Incluir una **línea de resumen** al final con: capital inicial, capital final, total comisiones, número de trades.

### 2.2 JSON completo (auditoría exhaustiva)

```json
{
  "meta": {
    "strategy": "SmaCrossover",
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "scenario_id": "bear_2022",
    "initial_capital": 10000,
    "params": { "fast_period": 20, "slow_period": 50 }
  },
  "trades": [ ... ],
  "equity_checkpoint": [
    { "timestamp": "...", "cash": 10000, "position": 0, "price": 29234, "equity": 10000 },
    { "timestamp": "...", "cash": 0, "position": 0.342, "price": 29234, "equity": 9997 },
    ...
  ]
}
```

- Útil para scripts de verificación automática.
- `equity_checkpoint`: un registro por vela (o solo donde hubo cambio) para reconstruir la curva.

### Botones en la UI

- **Descargar CSV** — solo trades.
- **Descargar JSON** — trades + equity + meta.
- **Copiar al portapapeles** — para pegar en Excel/Sheets.

---

## 3. Verificación de la secuencia de equity

### Fórmula que debe cumplirse

Para cada trade:

```
equity_despues = cash_despues + (posicion_despues × precio_mercado)
```

Para el **equity final**:

```
equity_final = capital_inicial + Σ(ganancia_por_trade) - Σ(comisiones)
```

Donde cada trade cerrado aporta:
- **BUY**: `-coste - comision` al cash
- **SELL**: `+coste - comision` al cash

### Herramienta: "Calculadora de verificación"

Panel en la UI donde el usuario puede:

1. **Pegar los primeros N trades** (o cargar el CSV descargado).
2. **Ver el cálculo paso a paso**:
   - Fila 0: Capital inicial = 10 000
   - Fila 1: Trade 1 → Cash = 10 000 - 9997 - 9.997 = 0 (aprox.)
   - Fila 2: Trade 2 → Cash = 0 + 9747 - 9.747 = 9737.25
3. **Comparar** el resultado con el equity que reporta el backtest.
4. **Indicador de coherencia**: ✓ "Los números cuadran" / ✗ "Discrepancia detectada".

### Tabla de equity por checkpoint

| Timestamp | Cash | Posición (amount) | Precio mercado | Equity calculado |
|-----------|------|-------------------|----------------|------------------|
| 2022-05-19 13:00 | 10000 | 0 | 29100 | 10000 |
| 2022-05-19 14:00 | 0 | 0.342 | 29234 | 9997 |
| 2022-05-20 08:00 | 9737.25 | 0 | 28500 | 9737.25 |

- El usuario puede elegir 2–3 filas y comprobar a mano: `equity = cash + position × price`.

---

## 4. Flujo de uso recomendado

1. Usuario ejecuta backtest (ej. SMA en Bear 2022).
2. Ve resultados: -25% return, 15 trades.
3. Activa **Modo Auditoría** (toggle o pestaña).
4. Ve la lista de decisiones con contexto (por qué cada trade).
5. Descarga el CSV de trades.
6. Abre en Excel, toma los 2–3 primeros trades.
7. Calcula manualmente:  
   - Trade 1: 10 000 - 9997 - 10 ≈ 0 ✓  
   - Trade 2: 0 + 9747 - 9.7 ≈ 9737 ✓  
8. Opcional: usa la "Calculadora de verificación" en la UI para contrastar.
9. Si todo cuadra → **confianza** en que el motor es coherente.

---

## 5. Cambios necesarios en el código

### Backend (FastAPI)

1. **Ampliar `SignalInfo`** (o crear `TradeAuditInfo`) con los campos de auditoría.
2. **En el loop del backtest**: guardar `cash_antes`, `posicion_antes`, indicadores en T, trigger (señal/TP/SL).
3. **Nuevo endpoint** `GET /api/backtest/audit/{run_id}` o incluir todo en la respuesta de `/run` (modo verbose).
4. **Endpoint de export** `GET /api/backtest/export?format=csv|json` que reciba los datos del último run (o un run_id).

### Frontend (React)

1. **Toggle "Modo Auditoría"** en la vista de resultados.
2. **Componente `AuditTradeList`**: tabla expandible con el detalle de cada trade.
3. **Botones**: Descargar CSV, Descargar JSON.
4. **Componente `EquityVerifier`**: inputs para pegar datos + cálculo paso a paso + indicador de coherencia.
5. **Tabla de checkpoints** de equity (opcional, puede ir en el JSON exportado).

### Persistencia (opcional)

- Guardar el último resultado de backtest en estado (React state / sessionStorage) para que los botones de export funcionen sin re-ejecutar.
- O pasar un `run_id` si se persisten runs en backend.

---

## 6. Resumen de entregables

| Entregable | Descripción |
|------------|-------------|
| Lista de decisiones con contexto | Por qué cada trade (señal, indicadores, regla) |
| Export CSV | Trades con columnas para verificación manual |
| Export JSON | Trades + equity checkpoints + meta |
| Calculadora de verificación | UI para comprobar que equity = cash + position × price |
| Tabla equity checkpoints | Ver evolución paso a paso del capital |

Con esto, el usuario puede **probar con sus propias manos** que la simulación es coherente y que los resultados son creíbles.
