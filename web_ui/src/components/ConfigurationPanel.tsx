import { History, Binary, ShieldCheck, Target, ChevronRight, Sparkles } from 'lucide-react'
import { NiceSelect } from './ui/NiceSelect'
import type { Discovery } from '../types'

interface ConfigurationPanelProps {
    discovery: Discovery | null
    config: any
    setConfig: (config: any) => void
    risk: any
    setRisk: (risk: any) => void
    runBacktest: () => void
    loading: boolean
    status: string
    handleStratChange: (id: string) => void
    guidedMode: boolean
    result: any
}

export function ConfigurationPanel({
    discovery, config, setConfig, risk, setRisk, runBacktest, loading, status, handleStratChange, guidedMode, result
}: ConfigurationPanelProps) {
    return (
        <aside className="col-span-12 lg:col-span-4 space-y-6">
            <section className="bg-slate-900 border border-white/5 p-8 rounded-[3rem] shadow-2xl space-y-10 relative overflow-hidden">
                <div className="relative z-10 space-y-8">
                    <div className="space-y-2">
                        <h2 className="text-xl font-black text-white tracking-tight flex items-center gap-3">
                            <History className="w-5 h-5 text-emerald-400" /> 1. Elige el Contexto
                        </h2>
                        <p className="text-xs text-slate-500 font-medium">¿Dónde quieres simular hoy?</p>
                    </div>

                    <div className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <NiceSelect label="Activo" value={config.symbol} onChange={(v: string) => setConfig({ ...config, symbol: v })} options={discovery?.available_symbols} />
                            <NiceSelect label="Frecuencia" value={config.timeframe} onChange={(v: string) => setConfig({ ...config, timeframe: v })} options={discovery?.available_timeframes} />
                        </div>
                        <NiceSelect label="Escenario Histórico" description="Carga periodos críticos grabados en el tiempo." value={config.scenario_id} onChange={(v: string) => setConfig({ ...config, scenario_id: v })} options={discovery?.scenarios.map(s => ({ label: s.label, value: s.id }))} />
                    </div>

                    <div className="pt-8 border-t border-white/5 space-y-6">
                        <div className="space-y-2">
                            <h2 className="text-xl font-black text-white tracking-tight flex items-center gap-3">
                                <Binary className="w-5 h-5 text-cyan-400" /> 2. Define la Estrategia
                            </h2>
                            <p className="text-xs text-slate-500 font-medium">¿Qué reglas debe seguir tu algoritmo?</p>
                        </div>

                        <div className="space-y-6">
                            <select
                                value={config.strategy_id}
                                onChange={e => handleStratChange(e.target.value)}
                                className="w-full bg-emerald-500/5 border-2 border-emerald-500/20 text-emerald-300 rounded-[1.5rem] px-6 py-4 text-sm font-black focus:ring-4 focus:ring-emerald-500/20 transition-all outline-none appearance-none"
                            >
                                {discovery?.strategies.map(s => <option key={s.id} value={s.id}>{s.label}</option>)}
                            </select>

                            {discovery?.strategies.find(s => s.id === config.strategy_id)?.parameters.length ? (
                                <div className="bg-slate-950/50 p-6 rounded-[2rem] border border-white/5 space-y-6">
                                    <p className="text-[10px] font-black text-slate-600 uppercase tracking-widest flex items-center gap-2"><Target className="w-4 h-4" /> Personalización</p>
                                    {discovery?.strategies.find(s => s.id === config.strategy_id)?.parameters.map(p => (
                                        <div key={p.name} className="space-y-3">
                                            <div className="flex justify-between items-center px-1">
                                                <label className="text-[11px] text-slate-400 font-black uppercase tracking-tight">{p.label}</label>
                                                <span className="text-[11px] font-mono text-emerald-400 font-bold">{config.params[p.name]}</span>
                                            </div>
                                            {p.type === 'number' ? (
                                                <input
                                                    type="range" min="1" max="200" step="1"
                                                    value={config.params[p.name]}
                                                    onChange={e => setConfig({ ...config, params: { ...config.params, [p.name]: parseFloat(e.target.value) } })}
                                                    className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-full appearance-none cursor-pointer"
                                                />
                                            ) : (
                                                <select
                                                    value={config.params[p.name]}
                                                    onChange={e => setConfig({ ...config, params: { ...config.params, [p.name]: e.target.value } })}
                                                    className="w-full bg-slate-900 border border-white/10 rounded-xl px-4 py-3 text-xs text-slate-300 outline-none"
                                                >
                                                    {p.options?.map(o => <option key={o} value={o}>{o}</option>)}
                                                </select>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            ) : null}
                        </div>
                    </div>

                    <div className="pt-8 border-t border-white/5 space-y-6">
                        <div className="space-y-2">
                            <h2 className="text-xl font-black text-white tracking-tight flex items-center gap-3">
                                <ShieldCheck className="w-5 h-5 text-rose-400" /> 3. Gestión de Riesgo
                            </h2>
                            <p className="text-xs text-slate-500 font-medium">Define tus salidas (Take Profit / Stop Loss)</p>
                        </div>
                        <div className="space-y-4 bg-slate-950/30 p-4 rounded-3xl border border-white/5">
                            {/* TP Controls */}
                            <div className="space-y-2">
                                <div className="flex justify-between items-center text-[10px] font-black uppercase text-emerald-500 tracking-widest">
                                    <span>Take Profit</span>
                                    {risk.tpType !== 'none' && <span>{risk.tpValue}{risk.tpType === 'percent' ? '%' : '$'}</span>}
                                </div>
                                <div className="flex gap-2">
                                    <select
                                        value={risk.tpType}
                                        onChange={e => setRisk({ ...risk, tpType: e.target.value })}
                                        className="bg-slate-900 text-xs rounded-lg px-2 py-2 border border-white/10 outline-none w-1/3"
                                    >
                                        <option value="none">Sin TP</option>
                                        <option value="percent">% PCT</option>
                                        <option value="absolute">$ USD</option>
                                    </select>
                                    {risk.tpType !== 'none' && (
                                        <input
                                            type="number"
                                            value={risk.tpValue}
                                            onChange={e => setRisk({ ...risk, tpValue: parseFloat(e.target.value) })}
                                            className="bg-slate-900 border border-white/10 rounded-lg px-3 py-2 text-xs w-2/3 outline-none text-right font-mono text-emerald-400 font-bold"
                                        />
                                    )}
                                </div>
                            </div>

                            {/* SL Controls */}
                            <div className="space-y-2 pt-2 border-t border-white/5">
                                <div className="flex justify-between items-center text-[10px] font-black uppercase text-rose-500 tracking-widest">
                                    <span>Stop Loss</span>
                                    {risk.slType !== 'none' && <span>{risk.slValue}{risk.slType === 'percent' ? '%' : '$'}</span>}
                                </div>
                                <div className="flex gap-2">
                                    <select
                                        value={risk.slType}
                                        onChange={e => setRisk({ ...risk, slType: e.target.value })}
                                        className="bg-slate-900 text-xs rounded-lg px-2 py-2 border border-white/10 outline-none w-1/3"
                                    >
                                        <option value="none">Sin SL</option>
                                        <option value="percent">% PCT</option>
                                        <option value="absolute">$ USD</option>
                                    </select>
                                    {risk.slType !== 'none' && (
                                        <input
                                            type="number"
                                            value={risk.slValue}
                                            onChange={e => setRisk({ ...risk, slValue: parseFloat(e.target.value) })}
                                            className="bg-slate-900 border border-white/10 rounded-lg px-3 py-2 text-xs w-2/3 outline-none text-right font-mono text-rose-400 font-bold"
                                        />
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>

                    <button
                        onClick={runBacktest}
                        disabled={loading || status === 'OFFLINE'}
                        className="w-full group bg-gradient-to-r from-emerald-600 to-cyan-600 hover:from-emerald-500 hover:to-cyan-500 text-white py-6 rounded-[2rem] font-black text-sm tracking-[0.2em] shadow-2xl shadow-emerald-500/20 transition-all hover:scale-[1.02] active:scale-95 flex items-center justify-center gap-4 disabled:opacity-20 disabled:grayscale"
                    >
                        {loading ? (
                            <div className="flex items-center gap-3">
                                <div className="w-5 h-5 border-3 border-white/20 border-t-white rounded-full animate-spin" />
                                PROCESANDO REALIDAD...
                            </div>
                        ) : (
                            <>VER CÓMO LE HABRÍA IDO <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" /></>
                        )}
                    </button>
                </div>
            </section>

            {/* INFO PARA EL USUARIO (GUIDED - ANTES DEL TEST) */}
            {guidedMode && !result && (
                <div className="bg-emerald-500/10 border border-emerald-500/20 p-8 rounded-[2.5rem] space-y-4 animate-in slide-in-from-left duration-500">
                    <h4 className="text-emerald-400 font-black text-sm flex items-center gap-2 underline underline-offset-8 mb-4 decoration-emerald-500/20">¿Nuevo por aquí?</h4>
                    <p className="text-xs text-emerald-200/60 leading-relaxed font-bold">
                        Este es tu tablero de experimentación. Elige una estrategia clásica como el <span className="text-white">RSI</span> y mira cómo el <span className="text-white">Régimen</span> del mercado (volatilidad) puede convertir una "buena idea" en cenizas.
                    </p>
                    <div className="pt-4 flex gap-3">
                        <div className="w-2 h-2 rounded-full bg-emerald-500 pulse" />
                        <span className="text-[10px] text-emerald-500 font-black uppercase">Prueba el Cruce de Medias en 1h</span>
                    </div>
                </div>
            )}

            {/* INFO PARA EL USUARIO (GUIDED - DESPUÉS DEL TEST) */}
            {guidedMode && result && (
                <div className="bg-cyan-500/10 border border-cyan-500/20 p-8 rounded-[2.5rem] space-y-6 animate-in slide-in-from-bottom duration-700">
                    <h4 className="text-cyan-400 font-black text-sm flex items-center gap-2 underline underline-offset-8 mb-4 decoration-cyan-500/20 italic">Guía de Interpretación</h4>
                    <div className="space-y-4">
                        <div className="flex gap-4">
                            <div className="w-8 h-8 rounded-lg bg-cyan-500/20 flex items-center justify-center shrink-0 text-cyan-400 font-black text-xs">1</div>
                            <p className="text-[11px] text-slate-400 font-medium leading-relaxed">
                                Mira la <span className="text-white">Curva de Equidad</span>. ¿Estás por encima de la línea punteada? Si no, habrías ganado más simplemente comprando y guardando el activo.
                            </p>
                        </div>
                        <div className="flex gap-4">
                            <div className="w-8 h-8 rounded-lg bg-cyan-500/20 flex items-center justify-center shrink-0 text-cyan-400 font-black text-xs">2</div>
                            <p className="text-[11px] text-slate-400 font-medium leading-relaxed">
                                Revisa el <span className="text-white">P-Value</span> abajo. Si es mayor a <span className="text-cyan-400">0.05</span>, tu algoritmo no ha hecho nada que un generador de números al azar no pudiera hacer.
                            </p>
                        </div>
                        <div className="flex gap-4">
                            <div className="w-8 h-8 rounded-lg bg-cyan-500/20 flex items-center justify-center shrink-0 text-cyan-400 font-black text-xs">3</div>
                            <p className="text-[11px] text-slate-400 font-medium leading-relaxed">
                                La <span className="text-white">Inacción</span> es clave. A veces el mejor trade es no operar. Ese número te dice cuánto dinero "salvaste" por quedarte fuera en momentos de pánico.
                            </p>
                        </div>
                    </div>
                    <div className="pt-4 flex gap-3 text-cyan-500 animate-pulse">
                        <Sparkles className="w-4 h-4" />
                        <span className="text-[9px] font-black uppercase">¡Sigue probando otros periodos!</span>
                    </div>
                </div>
            )}
        </aside>
    )
}
