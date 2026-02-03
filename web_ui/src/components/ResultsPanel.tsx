import { useMemo } from 'react'
import {
    XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Line, Area, ComposedChart, ReferenceLine
} from 'recharts'
import { Sparkles, ShieldCheck, Database, Scale } from 'lucide-react'
import { QuickMetric } from './ui/QuickMetric'
import { DetailedMetric } from './ui/DetailedMetric'
import type { BacktestResult } from '../types'

interface ResultsPanelProps {
    result: BacktestResult | null
    loading: boolean
    guidedMode: boolean
}

export function ResultsPanel({ result, loading, guidedMode }: ResultsPanelProps) {

    const chartData = useMemo(() => {
        if (!result) return []
        return result.equity_curve.map((v, i) => ({
            index: i,
            equity: v,
            benchmark: result.benchmark_curve[i],
            drawdown: result.drawdown_curve[i]
        }))
    }, [result])

    if (!result && !loading) {
        return (
            <div className="h-[700px] bg-slate-900/10 rounded-[4rem] border-4 border-dashed border-white/5 flex flex-col items-center justify-center text-center p-20 group relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-tr from-emerald-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                <div className="w-24 h-24 bg-slate-900/50 rounded-full flex items-center justify-center mb-10 border border-white/5 shadow-2xl scale-110 group-hover:scale-125 transition-transform duration-700">
                    <Sparkles className="w-10 h-10 text-slate-700 group-hover:text-emerald-400 transition-colors" />
                </div>
                <h2 className="text-4xl font-black text-white/50 mb-6 tracking-tighter">Tu simulación aparecerá aquí</h2>
                <p className="text-slate-600 max-w-md text-base leading-relaxed font-medium">Configura tu laboratorio en el panel izquierdo y pulsa el botón para ver la curva de resultados históricos.</p>
                <div className="mt-12 flex gap-8 items-center border-t border-white/5 pt-12">
                    <div className="text-center"><p className="text-[10px] text-slate-700 font-black uppercase tracking-widest mb-1">Cero Humo</p><ShieldCheck className="w-6 h-6 text-slate-800 mx-auto" /></div>
                    <div className="h-8 w-px bg-white/5" />
                    <div className="text-center"><p className="text-[10px] text-slate-700 font-black uppercase tracking-widest mb-1">Datos Reales</p><Database className="w-6 h-6 text-slate-800 mx-auto" /></div>
                    <div className="h-8 w-px bg-white/5" />
                    <div className="text-center"><p className="text-[10px] text-slate-700 font-black uppercase tracking-widest mb-1">Sin Mentiras</p><Scale className="w-6 h-6 text-slate-800 mx-auto" /></div>
                </div>
            </div>
        )
    }

    if (!result) return null

    return (
        <section className="bg-slate-900 border border-white/5 rounded-[4rem] p-12 shadow-2xl relative overflow-hidden">
            {guidedMode && (
                <div className="absolute top-8 right-12 z-20 flex gap-2">
                    <span className="bg-cyan-500/20 border border-cyan-500/40 text-cyan-400 px-4 py-1.5 rounded-full text-[9px] font-black uppercase tracking-widest shadow-lg shadow-cyan-500/10">Compare contra el mercado</span>
                </div>
            )}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-8 mb-12 relative z-10">
                <div className="space-y-1">
                    <h3 className="text-2xl font-black text-white flex items-center gap-3 tracking-tighter">
                        Resultado de la Simulación
                        <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                    </h3>
                    <p className="text-xs text-slate-500 font-bold uppercase tracking-widest">Comparativa contra el Mercado (Hold)</p>
                </div>
                <div className="flex gap-4">
                    <QuickMetric label="Crecimiento" value={`${result.total_return}%`} positive={result.total_return >= 0}
                        tooltip={guidedMode ? "Cuánto dinero has ganado o perdido en total respecto a tus 10k iniciales." : ""} />
                    <QuickMetric label="Benchmark" value={`${result.benchmark_return.toFixed(1)}%`} neutral
                        tooltip={guidedMode ? "Qué habría pasado si solo compras y guardas (Buy & Hold)." : ""} />
                </div>
            </div>

            <div className="h-[400px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <ComposedChart data={chartData}>
                        <defs>
                            <linearGradient id="mainGrad" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.02)" vertical={false} />
                        <XAxis hide />
                        <YAxis hide domain={['dataMin - 200', 'dataMax + 200']} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#020617', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '24px', padding: '20px', boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)' }}
                            itemStyle={{ fontSize: '12px', fontWeight: '800', textTransform: 'uppercase' }}
                        />
                        <Area type="stepAfter" dataKey="equity" name="Tu Estrategia" stroke="#10b981" strokeWidth={4} fill="url(#mainGrad)" isAnimationActive />
                        <Line type="monotone" dataKey="benchmark" name="Hold" stroke="rgba(255,255,255,0.1)" strokeWidth={2} strokeDasharray="6 6" dot={false} />
                        <ReferenceLine y={10000} stroke="rgba(255,255,255,0.05)" strokeWidth={1} />
                    </ComposedChart>
                </ResponsiveContainer>
            </div>

            <div className="mt-12 pt-12 border-t border-white/5 flex flex-wrap gap-8 justify-between items-center text-center">
                <DetailedMetric label="Max Caída" value={`${result.max_drawdown}%`} desc="El peor momento del viaje"
                    info={guidedMode ? "El máximo susto. La mayor caída que tuvo tu capital desde su punto más alto." : ""} />
                <div className="h-8 w-px bg-white/5" />
                <DetailedMetric label="Eficiencia (Sharpe)" value={result.sharpe_ratio.toFixed(2)} desc="Retorno por cada gota de riesgo"
                    info={guidedMode ? "Mide la calidad. ¿Ganas dinero consistentemente o por pura suerte volátil? > 1 es excelente." : ""} />
                <div className="h-8 w-px bg-white/5" />
                <DetailedMetric label="Decisiones" value={result.total_trades} desc="Trades ejecutados en total"
                    info={guidedMode ? "Cuántas veces el algoritmo entró y salió del mercado." : ""} />
                <div className="h-8 w-px bg-white/5" />
                <DetailedMetric label="Inacción" value={`+${result.inaction_value.toFixed(1)}%`} desc="Dinero salvado por no operar"
                    info={guidedMode ? "Tu escudo. Cuánto dinero evitaste perder al no estar operando durante las caídas." : ""} />
            </div>

            {/* Advanced Risk Metrics Row */}
            <div className="mt-8 pt-6 border-t border-white/5 grid grid-cols-4 gap-4 text-center">
                <div className="bg-slate-950/50 p-3 rounded-2xl">
                    <p className="text-[9px] uppercase tracking-widest text-slate-600 font-bold">Tiempo en Pérdida</p>
                    <p className="text-sm font-black text-rose-400 font-mono mt-1">{result.time_in_loss_pct.toFixed(1)}%</p>
                </div>
                <div className="bg-slate-950/50 p-3 rounded-2xl">
                    <p className="text-[9px] uppercase tracking-widest text-slate-600 font-bold">Latent Drawdown</p>
                    <p className="text-sm font-black text-amber-500 font-mono mt-1">{result.max_latent_drawdown.toFixed(1)}%</p>
                </div>
                <div className="bg-slate-950/50 p-3 rounded-2xl">
                    <p className="text-[9px] uppercase tracking-widest text-slate-600 font-bold">Duración Promedio</p>
                    <p className="text-sm font-black text-slate-300 font-mono mt-1">{result.avg_trade_duration_candles.toFixed(1)}h</p>
                </div>
                <div className="bg-slate-950/50 p-3 rounded-2xl">
                    <p className="text-[9px] uppercase tracking-widest text-slate-600 font-bold">Exposición Max</p>
                    <p className="text-sm font-black text-cyan-400 font-mono mt-1">${Math.round(result.max_money_at_risk).toLocaleString()}</p>
                </div>
            </div>
        </section>
    )
}
