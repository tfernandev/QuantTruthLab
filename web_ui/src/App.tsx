import { useState, useEffect } from 'react'
import axios from 'axios'
import type { BacktestResult, Discovery } from './types'
import { Header } from './components/Header'
import { ConfigurationPanel } from './components/ConfigurationPanel'
import { ResultsPanel } from './components/ResultsPanel'
import { DiagnosisPanel } from './components/DiagnosisPanel'
import { TradeHistory, DisclaimerFooter } from './components/TradeHistory'
import { AuditPanel } from './components/AuditPanel'

// Use ENV variable
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export default function QuantTruthTerminal() {
    const [discovery, setDiscovery] = useState<Discovery | null>(null)
    const [config, setConfig] = useState<any>({
        symbol: 'BTC/USDT',
        strategy_id: '',
        scenario_id: '',
        timeframe: '1h',
        params: {}
    })
    // Risk Config
    const [risk, setRisk] = useState({
        tpType: 'none', tpValue: 10.0,
        slType: 'none', slValue: 5.0
    })
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState<BacktestResult | null>(null)
    const [status, setStatus] = useState<'ONLINE' | 'OFFLINE'>('OFFLINE')
    const [guidedMode, setGuidedMode] = useState(false)
    const [auditMode, setAuditMode] = useState(false)

    useEffect(() => {
        axios.get(`${API_URL}/discovery/`).then(res => {
            setDiscovery(res.data)
            setStatus('ONLINE')
            if (res.data.strategies.length > 0) {
                const s = res.data.strategies[0]
                const dp = {} as any
                s.parameters.forEach((p: any) => dp[p.name] = p.default)
                setConfig({
                    strategy_id: s.id,
                    scenario_id: res.data.scenarios[0].id,
                    symbol: res.data.available_symbols[0] || 'BTC/USDT',
                    timeframe: '1h',
                    params: dp
                })
            }
        }).catch(() => setStatus('OFFLINE'))
    }, [])

    const handleStratChange = (id: string) => {
        const s = discovery?.strategies.find(x => x.id === id)
        const dp = {} as any
        s?.parameters.forEach(p => dp[p.name] = p.default)
        setConfig({ ...config, strategy_id: id, params: dp })
    }

    const runBacktest = async () => {
        setLoading(true)
        setResult(null)
        try {
            const res = await axios.post(`${API_URL}/backtest/run/`, {
                symbol: config.symbol,
                timeframe: config.timeframe,
                strategy_name: config.strategy_id,
                scenario_id: config.scenario_id,
                params: config.params,
                initial_capital: 10000,
                // Risk Props
                tp_type: risk.tpType === 'none' ? undefined : risk.tpType,
                tp_value: risk.tpType === 'none' ? undefined : Number(risk.tpValue),
                sl_type: risk.slType === 'none' ? undefined : risk.slType,
                sl_value: risk.slType === 'none' ? undefined : Number(risk.slValue),
            })
            setResult(res.data)
        } catch (e: any) {
            alert(e.response?.data?.detail || "Error en el motor")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-[#020617] text-slate-300 font-sans selection:bg-emerald-500/30">
            {/* -- GLOW EFFECTS -- */}
            <div className="fixed top-0 left-1/4 w-96 h-96 bg-emerald-500/5 blur-[120px] pointer-events-none" />
            <div className="fixed bottom-0 right-1/4 w-96 h-96 bg-cyan-500/5 blur-[120px] pointer-events-none" />

            <div className="max-w-[1500px] mx-auto p-4 lg:p-10 space-y-10 relative z-10">

                <Header guidedMode={guidedMode} setGuidedMode={setGuidedMode} />

                <div className="grid grid-cols-12 gap-8">

                    <ConfigurationPanel
                        discovery={discovery}
                        config={config}
                        setConfig={setConfig}
                        risk={risk}
                        setRisk={setRisk}
                        runBacktest={runBacktest}
                        loading={loading}
                        status={status}
                        handleStratChange={handleStratChange}
                        guidedMode={guidedMode}
                        result={result}
                    />

                    {/* --- MAIN STAGE (EXPLORE MODE) --- */}
                    <div className="col-span-12 lg:col-span-8 space-y-8">

                        <ResultsPanel result={result} loading={loading} guidedMode={guidedMode} />

                        {result && (
                            <div className="space-y-8 animate-in fade-in zoom-in-95 duration-700">

                                <div className="flex justify-end px-4">
                                    <button
                                        onClick={() => setAuditMode(!auditMode)}
                                        className={`flex items-center gap-2 px-6 py-2 rounded-full text-xs font-black uppercase tracking-widest transition-all border ${auditMode ? 'bg-white text-slate-900 border-white' : 'bg-transparent text-slate-500 border-slate-700 hover:border-slate-500 hover:text-slate-300'}`}
                                    >
                                        {auditMode ? 'Ocultar Auditoría' : '🔍 Activar Modo Auditoría'}
                                    </button>
                                </div>

                                {auditMode && <AuditPanel result={result} />}

                                <DiagnosisPanel result={result} guidedMode={guidedMode} />
                                {!auditMode && <TradeHistory result={result} />}
                                <DisclaimerFooter />
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* FLOATING STATUS */}
            <div className="fixed bottom-8 left-8 p-4 bg-slate-900/80 backdrop-blur-3xl border border-white/10 rounded-2xl flex items-center gap-4 shadow-2xl z-50">
                <div className={`w-3 h-3 rounded-full ${status === 'ONLINE' ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
                <span className="text-[10px] font-black uppercase text-slate-400 tracking-widest">Truth Engine {status === 'ONLINE' ? 'Conectado' : 'Offline'}</span>
            </div>
        </div>
    )
}
