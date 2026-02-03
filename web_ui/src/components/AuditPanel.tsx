import { useState } from 'react'
import { Download, Calculator, CheckCircle2, ChevronDown, ChevronUp, Search, FileJson } from 'lucide-react'
import type { BacktestResult, Signal } from '../types'

interface AuditPanelProps {
    result: BacktestResult
}

export function AuditPanel({ result }: AuditPanelProps) {
    const [view, setView] = useState<'trades' | 'verify'>('trades')

    const downloadCSV = () => {
        const headers = ["idx", "timestamp", "trigger", "side", "price", "amount", "cost", "commission", "cash_before", "cash_after", "pos_before", "pos_after", "equity_after", "rule"]
        const rows = result.signals.map((s, i) => [
            i + 1,
            s.timestamp,
            s.trigger,
            s.side,
            s.price,
            s.amount,
            s.cost,
            s.commission,
            s.cash_before,
            s.cash_after,
            s.pos_before,
            s.pos_after,
            s.equity_after,
            `"${s.rule || ''}"` // Escape quotes
        ].join(","))

        const csvContent = "data:text/csv;charset=utf-8," + headers.join(",") + "\n" + rows.join("\n")
        const encodedUri = encodeURI(csvContent)
        const link = document.createElement("a")
        link.setAttribute("href", encodedUri)
        link.setAttribute("download", `audit_trades_${new Date().toISOString().slice(0, 10)}.csv`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }

    const downloadJSON = () => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(result, null, 2))
        const link = document.createElement("a")
        link.setAttribute("href", dataStr)
        link.setAttribute("download", `audit_full_${new Date().toISOString().slice(0, 10)}.json`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }

    return (
        <section className="bg-slate-900 border border-white/5 rounded-[3rem] p-8 shadow-2xl relative overflow-hidden space-y-8">
            <div className="flex justify-between items-center border-b border-white/5 pb-6">
                <div>
                    <h3 className="text-2xl font-black text-white flex items-center gap-3">
                        <CheckCircle2 className="w-6 h-6 text-emerald-500" />
                        Modo Auditoría
                    </h3>
                    <p className="text-xs text-slate-500 font-bold uppercase tracking-widest mt-1">Verificación Forense de Resultados</p>
                </div>
                <div className="flex gap-2">
                    <button
                        onClick={() => setView('trades')}
                        className={`px-4 py-2 rounded-xl text-xs font-black transition-all ${view === 'trades' ? 'bg-slate-800 text-white' : 'text-slate-500 hover:text-slate-300'}`}
                    >
                        Registro de Trades
                    </button>
                    <button
                        onClick={() => setView('verify')}
                        className={`px-4 py-2 rounded-xl text-xs font-black transition-all ${view === 'verify' ? 'bg-slate-800 text-white' : 'text-slate-500 hover:text-slate-300'}`}
                    >
                        Calculadora
                    </button>
                </div>
            </div>

            {view === 'trades' ? (
                <div className="space-y-6">
                    <div className="flex gap-4">
                        <button onClick={downloadCSV} className="flex items-center gap-2 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 px-4 py-2 rounded-lg text-xs font-black transition-colors border border-emerald-500/20">
                            <Download className="w-4 h-4" /> Exportar CSV
                        </button>
                        <button onClick={downloadJSON} className="flex items-center gap-2 bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 px-4 py-2 rounded-lg text-xs font-black transition-colors border border-cyan-500/20">
                            <FileJson className="w-4 h-4" /> Exportar JSON Completo
                        </button>
                    </div>
                    <TradeList signals={result.signals} />
                </div>
            ) : (
                <EquityVerifier />
            )}
        </section>
    )
}

function TradeList({ signals }: { signals: Signal[] }) {
    const [expandedIds, setExpandedIds] = useState<number[]>([])
    const [searchTerm, setSearchTerm] = useState('')

    const toggleExpand = (idx: number) => {
        setExpandedIds(prev => prev.includes(idx) ? prev.filter(i => i !== idx) : [...prev, idx])
    }

    const filteredSignals = signals.filter(s =>
        s.timestamp.includes(searchTerm) ||
        s.trigger?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        s.side.toLowerCase().includes(searchTerm.toLowerCase())
    )

    return (
        <div className="space-y-4">
            <div className="relative">
                <Search className="absolute left-3 top-3 w-4 h-4 text-slate-500" />
                <input
                    type="text"
                    placeholder="Buscar por fecha, tipo..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                    className="w-full bg-slate-950 border border-white/10 rounded-xl pl-10 pr-4 py-2.5 text-xs text-slate-300 outline-none focus:border-emerald-500/50 transition-colors"
                />
            </div>

            <div className="space-y-2 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
                {filteredSignals.map((s, idx) => (
                    <div key={idx} className="bg-slate-950/50 border border-white/5 rounded-2xl overflow-hidden">
                        <div
                            onClick={() => toggleExpand(idx)}
                            className="p-4 flex items-center justify-between cursor-pointer hover:bg-white/5 transition-colors gap-4"
                        >
                            <div className="flex items-center gap-4 flex-1">
                                <div className={`w-8 h-8 rounded-lg flex items-center justify-center text-[10px] font-black ${s.side === 'BUY' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'}`}>
                                    {s.side.substring(0, 1)}
                                </div>
                                <div>
                                    <div className="text-xs font-mono font-bold text-slate-300">{s.timestamp}</div>
                                    <div className="text-[10px] text-slate-500 font-black uppercase tracking-wider">{s.trigger}</div>
                                </div>
                            </div>

                            <div className="text-right">
                                <div className="text-xs font-mono font-black text-white">${s.price.toLocaleString(undefined, { minimumFractionDigits: 2 })}</div>
                                <div className="text-[10px] text-slate-500">{s.amount?.toFixed(4)} units</div>
                            </div>

                            {expandedIds.includes(idx) ? <ChevronUp className="w-4 h-4 text-slate-500" /> : <ChevronDown className="w-4 h-4 text-slate-500" />}
                        </div>

                        {expandedIds.includes(idx) && (
                            <div className="bg-slate-900/80 p-6 border-t border-white/5 grid grid-cols-1 md:grid-cols-2 gap-8 animate-in slide-in-from-top-2 duration-200">
                                <div className="space-y-4">
                                    <h4 className="text-[10px] font-black text-slate-500 uppercase tracking-widest border-b border-white/5 pb-2">Detalles Financieros</h4>
                                    <div className="grid grid-cols-2 gap-y-2 text-[11px]">
                                        <div className="text-slate-500">Comisión (0.1%):</div>
                                        <div className="text-right font-mono text-rose-400">-${s.commission?.toFixed(2)}</div>

                                        <div className="text-slate-500">Cash Antes:</div>
                                        <div className="text-right font-mono text-slate-400">${s.cash_before?.toFixed(2)}</div>

                                        <div className="text-slate-500">Cash Después:</div>
                                        <div className="text-right font-mono text-white">${s.cash_after?.toFixed(2)}</div>

                                        <div className="text-slate-500">Equity Snapshot:</div>
                                        <div className="text-right font-mono text-emerald-400 font-bold">${s.equity_after?.toFixed(2)}</div>
                                    </div>
                                </div>

                                <div className="space-y-4">
                                    <h4 className="text-[10px] font-black text-slate-500 uppercase tracking-widest border-b border-white/5 pb-2">Contexto de Decisión</h4>
                                    <div className="space-y-3">
                                        <div className="bg-slate-950 p-3 rounded-lg border border-white/5">
                                            <p className="text-[10px] text-slate-500 uppercase mb-1">Regla Aplicada</p>
                                            <p className="text-xs font-medium text-slate-300 italic">"{s.rule}"</p>
                                        </div>
                                        {s.indicators && (
                                            <div className="grid grid-cols-2 gap-2">
                                                {Object.entries(s.indicators).map(([k, v]) => (
                                                    <div key={k} className="flex justify-between bg-slate-950 p-2 rounded border border-white/5">
                                                        <span className="text-[9px] text-slate-500 font-bold">{k}</span>
                                                        <span className="text-[9px] font-mono text-cyan-400">{v.toFixed(2)}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    )
}

function EquityVerifier() {
    const [startCapital, setStartCapital] = useState(10000)
    const [tradesInput, setTradesInput] = useState('')
    const [calculation, setCalculation] = useState<any[]>([])

    // Format: PRICE, AMT, SIDE ('BUY'/'SELL'), COMM
    // Simple verification tool

    const verify = () => {
        let cash = startCapital
        let pos = 0
        const log = []

        const lines = tradesInput.split('\n').filter(l => l.trim().length > 0)

        log.push({ step: 'Inicio', cash, pos, equity: cash, explanation: 'Capital Inicial' })

        for (const line of lines) {
            // Expected format: SIDE PRICE AMT (e.g. BUY 29000 0.1)
            const parts = line.trim().split(/\s+/)
            if (parts.length < 3) continue

            const side = parts[0].toUpperCase()
            const price = parseFloat(parts[1])
            const amt = parseFloat(parts[2])
            const comm = price * amt * 0.001 // Approx 0.1%

            let explanation = ''

            if (side === 'BUY') {
                cash = cash - (price * amt) - comm
                pos += amt
                explanation = `Compra ${amt} @ ${price} (Comm: ${comm.toFixed(2)})`
            } else {
                cash = cash + (price * amt) - comm
                pos -= amt
                explanation = `Venta ${amt} @ ${price} (Comm: ${comm.toFixed(2)})`
            }

            const equity = cash + (pos * price)
            log.push({ step: `Trade ${log.length}`, cash, pos, equity, explanation })
        }

        setCalculation(log)
    }

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <div className="bg-emerald-500/10 border border-emerald-500/20 p-6 rounded-2xl">
                <h4 className="flex items-center gap-2 text-emerald-400 font-black text-sm mb-2">
                    <Calculator className="w-4 h-4" /> Calculadora de la Verdad
                </h4>
                <p className="text-xs text-slate-400 leading-relaxed">
                    Usa esta herramienta para verificar manualmente que el motor no inventa dinero.
                    Copia algunos trades del CSV y pégalos aquí en formato: <code className="bg-black/30 px-1 rounded text-emerald-300">SIDE PRICE AMOUNT</code>.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="space-y-4">
                    <div className="space-y-2">
                        <label className="text-[10px] font-black uppercase text-slate-500 tracking-widest">Capital Inicial</label>
                        <input
                            type="number"
                            value={startCapital}
                            onChange={e => setStartCapital(parseFloat(e.target.value))}
                            className="w-full bg-slate-950 border border-white/10 p-3 rounded-xl text-sm font-mono text-white outline-none"
                        />
                    </div>
                    <div className="space-y-2">
                        <label className="text-[10px] font-black uppercase text-slate-500 tracking-widest">Pegar Trades (BUY/SELL PRECIO CANTIDAD)</label>
                        <textarea
                            value={tradesInput}
                            onChange={e => setTradesInput(e.target.value)}
                            placeholder={`BUY 29000 0.1\nSELL 30000 0.1`}
                            className="w-full h-48 bg-slate-950 border border-white/10 p-3 rounded-xl text-xs font-mono text-slate-300 outline-none"
                        />
                    </div>
                    <button
                        onClick={verify}
                        className="w-full bg-slate-800 hover:bg-slate-700 text-white font-black py-3 rounded-xl text-xs uppercase tracking-widest transition-colors"
                    >
                        Calcular Secuencia
                    </button>
                </div>

                <div className="bg-slate-950 border border-white/5 rounded-2xl overflow-hidden">
                    <div className="bg-slate-900 px-4 py-3 border-b border-white/5 text-[10px] font-black uppercase tracking-widest text-slate-500 flex justify-between">
                        <span>Paso</span>
                        <span>Equity Resultante</span>
                    </div>
                    <div className="divide-y divide-white/5">
                        {calculation.map((row, idx) => (
                            <div key={idx} className="px-4 py-3 flex justify-between items-center hover:bg-white/5 transition-colors">
                                <div>
                                    <div className="text-[11px] font-bold text-slate-300">{row.step}</div>
                                    <div className="text-[9px] text-slate-500">{row.explanation}</div>
                                </div>
                                <div className="text-right">
                                    <div className="text-xs font-mono font-black text-emerald-400">${row.equity.toFixed(2)}</div>
                                    <div className="text-[9px] text-slate-600 font-mono">Cash: ${row.cash.toFixed(2)}</div>
                                </div>
                            </div>
                        ))}
                        {calculation.length === 0 && (
                            <div className="p-8 text-center text-xs text-slate-600 italic">
                                Esperando datos para calcular...
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}
