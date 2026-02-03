import ccxt
import pandas as pd
import pandas_ta as ta
from datetime import datetime

def check_truth():
    logit = []
    def log(msg):
        print(msg)
        logit.append(str(msg))
        
    log("--- VERIFICACION INDEPENDIENTE DE DATOS (2021) ---")
    log("Conectando con Binance (Data Publica) via CCXT...")
    
    exchange = ccxt.binance()
    symbol = 'BTC/USDT'
    timeframe = '1h'
    start_date = '2021-01-01T00:00:00Z'
    end_date = '2021-12-31T23:59:59Z'
    
    since = exchange.parse8601(start_date)
    end_ts = exchange.parse8601(end_date)
    
    all_ohlcv = []
    
    log(f"Descargando velas de 1h para {symbol} desde {start_date}...")
    
    while since < end_ts:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit=1000)
            if not ohlcv:
                break
            since = ohlcv[-1][0] + 1  # Next timestamp
            all_ohlcv.extend(ohlcv)
            print(f"Descargados {len(all_ohlcv)} velas...", end='\r')
            if len(ohlcv) < 1000:
                break
        except Exception as e:
            log(f"Error fetching data: {e}")
            break
            
    log(f"\nTotal velas descargadas: {len(all_ohlcv)}")
    
    if not all_ohlcv:
        log("No se pudieron descargar datos.")
        return

    df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df[df['timestamp'] <= end_ts] # Cutoff exact end
    df.set_index('datetime', inplace=True)
    
    # 1. BENCHMARK CHECK
    start_price = df['close'].iloc[0]
    end_price = df['close'].iloc[-1]
    
    bench_return = ((end_price - start_price) / start_price) * 100
    
    log(f"\nDATOS REALES (Binance):")
    log(f"Precio Inicio (2021-01-01): ${start_price:.2f}")
    log(f"Precio Fin    (2021-12-31): ${end_price:.2f}")
    log(f"Rendimiento REAL (Buy & Hold): {bench_return:.2f}%")
    log("NOTA: El sistema muestra 59.4%. Si este numero es cercano (57-60%), el simulador tiene datos correctos.")
    
    # 2. STRATEGY CHECK (Approximation)
    # SMA 10 vs 133
    log("\n--- SIMULACION RAPIDA DE ESTRATEGIA (10/133) ---")
    df['fast_sma'] = ta.sma(df['close'], length=10)
    df['slow_sma'] = ta.sma(df['close'], length=133)
    
    # Signal: 1 if Fast > Slow, 0 otherwise (assuming Long/Flat)
    df['signal'] = 0
    df.loc[df['fast_sma'] > df['slow_sma'], 'signal'] = 1
    
    # Shift signal to avoid lookahead bias (trade occurs next candle)
    df['position'] = df['signal'].shift(1)
    
    # Hourly returns
    df['pct_change'] = df['close'].pct_change()
    
    # Strategy returns
    df['strat_ret'] = df['position'] * df['pct_change']
    
    # Cumulative Return (Compounded)
    df['cum_bench'] = (1 + df['pct_change']).cumprod()
    df['cum_strat'] = (1 + df['strat_ret']).cumprod()
    
    total_strat_return = (df['cum_strat'].iloc[-1] - 1) * 100
    
    log(f"Estrategia (Long Only) Estimada: {total_strat_return:.2f}%")
    
    # Check Trades count
    trades = df['signal'].diff().abs().sum() / 2 # Approx
    log(f"Trades Estimados: ~{int(trades)}")
    
    # Check Drawdown
    rolling_max = df['cum_strat'].cummax()
    drawdown = (df['cum_strat'] - rolling_max) / rolling_max
    max_dd = drawdown.min() * 100
    log(f"Max Drawdown Estimado: {max_dd:.2f}%")
    
    log("\nCONCLUSION:")
    if abs(bench_return - 59.4) < 5:
        log("[OK] El Benchmark del sistema es muy preciso.")
    else:
        log("[ALERTA] Hay una discrepancia en el Benchmark.")
        
    if total_strat_return < 0:
        log("[INFO] La estrategia pierde dinero en la realidad tambien (Long Only).")
        log("   Explicacion: En un mercado volatil, una media rapida (10h) cruza muchas veces y genera perdidas por falsas senales.")
    else:
        log(f"[INFO] Nuestra simulacion simple da positivo ({total_strat_return:.2f}%).")
        log("   Si el sistema da negativo (-15%), puede ser por:")
        log("   1. Comisiones (Fees) - Nuestra simulacion simple no incluye fees.")
        log("   2. Slippage.")
        log("   3. La logica exacta (quizas cierra posicion tarde).")
        
    with open("verify_truth_log.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(logit))

if __name__ == "__main__":
    check_truth()
