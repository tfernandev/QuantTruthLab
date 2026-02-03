import { Navigation, AlertTriangle } from 'lucide-react'
import type { BacktestResult } from '../types'

interface TradeHistoryProps {
    result: BacktestResult
}

export function TradeHistory({ result }: TradeHistoryProps) {
    if (!result) return null

    return (
        <section className="bg-slate-900/40 border border-white/5 rounded-[4rem] p-12">
            <div className="flex justify-between items-center mb-8">
                <div className="flex items-center gap-4">
                    <Navigation className="w-5 h-5 text-slate-500" />
                    <h3 className="text-xl font-black text-white tracking-tight">Rastro de Decisiones</h3>
                </div>
                <p className="text-[10px] font-mono text-slate-700 uppercase tracking-widest font-black">Histórico de Últimos 15 Trades</p>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
                {result.signals.slice(-15).reverse().map((s, i) => (
                    <div key={i} className={`p-5 rounded-3xl border transition-all hover:scale-105 ${s.side === 'BUY' ? 'bg-emerald-500/5 border-emerald-500/20 text-emerald-300' : 'bg-rose-500/5 border-rose-500/20 text-rose-300'}`}>
                        <div className="text-[9px] font-black uppercase opacity-40 mb-2">{s.side} Signal</div>
                        <div className="text-base font-black font-mono tracking-tighter">${s.price.toLocaleString()}</div>
                        <div className="text-[8px] mt-2 font-bold opacity-30">{new Date(s.timestamp).toLocaleDateString()}</div>
                    </div>
                ))}
            </div>
        </section>
    )
}

export function DisclaimerFooter() {
    return (
        <footer className="bg-white/5 border border-white/5 rounded-[3rem] p-10 flex gap-10 items-center">
            <AlertTriangle className="w-16 h-16 text-slate-700 shrink-0" />
            <div className="space-y-4">
                <h5 className="text-[11px] font-black text-slate-400 uppercase tracking-widest">¿Qué has aprendido hoy?</h5>
                <p className="text-xs text-slate-600 leading-relaxed font-medium uppercase italic tracking-tighter">
                    Este terminal no es una promesa de ganancias. Es una herramienta educativa para demostrar que la mayoría de los indicadores clásicos fallan contra el mercado o contra el puro azar tras comisiones. Si ves números rojos, felicidades: acabas de ahorrarte dinero que habrías perdido operando a ciegas.
                </p>
            </div>
        </footer>
    )
}
