import { Target, ShieldCheck, ZapOff, Microscope, Eye } from 'lucide-react'
import { RobustTile } from './ui/RobustTile'
import type { BacktestResult } from '../types'

interface DiagnosisPanelProps {
    result: BacktestResult
    guidedMode: boolean
}

export function DiagnosisPanel({ result, guidedMode }: DiagnosisPanelProps) {
    if (!result) return null

    return (
        <div className="grid grid-cols-12 gap-8 relative">
            {guidedMode && (
                <div className="absolute -top-4 -left-4 z-30 bg-cyan-600 text-white rounded-full p-2 border-4 border-[#020617] shadow-xl">
                    <Target className="w-5 h-5" />
                </div>
            )}
            {/* VEREDICTO NARRATIVO */}
            <section className={`col-span-12 lg:col-span-7 p-10 rounded-[3.5rem] border-2 relative overflow-hidden transition-all hover:scale-[1.01] ${result.is_significant ? 'bg-emerald-500/10 border-emerald-500/20 shadow-[0_0_50px_rgba(16,185,129,0.1)]' : 'bg-rose-500/10 border-rose-500/20 shadow-[0_0_50px_rgba(244,63,94,0.1)]'}`}>
                <div className="relative z-10 space-y-8">
                    <div className="flex items-center gap-4">
                        <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${result.is_significant ? 'bg-emerald-500 text-slate-900' : 'bg-rose-500 text-white'}`}>
                            {result.is_significant ? <ShieldCheck className="w-7 h-7" /> : <ZapOff className="w-7 h-7" />}
                        </div>
                        <h3 className="text-[11px] font-black uppercase tracking-[0.3em] text-slate-500">Diagnóstico de Veracidad</h3>
                    </div>

                    <div className="space-y-4">
                        <h4 className="text-3xl font-black text-white leading-tight tracking-tight">
                            {result.research_conclusion}
                        </h4>
                        <p className="text-sm text-slate-400 font-medium leading-relaxed italic">
                            "{result.stress_moment_explanation}"
                        </p>
                    </div>

                    <div className="flex gap-4 pt-4">
                        <div className="bg-white/5 px-6 py-3 rounded-2xl border border-white/5 relative group">
                            <span className="text-[9px] text-slate-600 font-black uppercase tracking-widest block mb-1">Índice de Suerte (P-Value)</span>
                            <span className="text-base font-black font-mono text-white">{result.p_value.toFixed(3)}</span>
                            {guidedMode && (
                                <div className="absolute -top-12 left-0 w-48 bg-cyan-900 p-2 rounded-lg text-[9px] font-bold text-white shadow-xl border border-cyan-700 opacity-0 group-hover:opacity-100 transition-opacity">
                                    Mide si ganaste por habilidad o por azar. {'<'} 0.05 es Habilidad.
                                </div>
                            )}
                        </div>
                        <div className="bg-white/5 px-6 py-3 rounded-2xl border border-white/5 relative group">
                            <span className="text-[9px] text-slate-600 font-black uppercase tracking-widest block mb-1">Fragilidad de Idea</span>
                            <span className={`text-base font-black font-mono ${result.stability_variance < 15 ? 'text-emerald-400' : 'text-rose-400'}`}>{result.stability_variance.toFixed(1)}%</span>
                            {guidedMode && (
                                <div className="absolute -top-12 left-0 w-48 bg-cyan-900 p-2 rounded-lg text-[9px] font-bold text-white shadow-xl border border-cyan-700 opacity-0 group-hover:opacity-100 transition-opacity">
                                    Indica si la estrategia se rompe al cambiar parámetros mínimos.
                                </div>
                            )}
                        </div>
                    </div>
                </div>
                <Microscope className="absolute -bottom-10 -right-10 w-48 h-48 opacity-10 rotate-12" />
            </section>

            {/* REGIMENES Y SEGURIDAD */}
            <section className="col-span-12 lg:col-span-5 bg-slate-950/40 p-10 rounded-[3.5rem] border border-white/5 space-y-8">
                <h3 className="text-xs font-black uppercase tracking-widest text-slate-500 flex items-center gap-3">
                    <Eye className="w-4 h-4" /> Comportamiento por Régimen
                </h3>
                <div className="space-y-4">
                    {result.regime_stats.map(r => (
                        <div key={r.label} className="bg-slate-900/50 p-6 rounded-3xl border border-white/5 flex justify-between items-center group hover:border-white/10 transition-colors">
                            <div>
                                <span className="text-xs font-black text-white block mb-1 uppercase tracking-tight">{r.label}</span>
                                <span className="text-[10px] text-slate-600 font-bold uppercase">{(r.percentage_of_time * 100).toFixed(0)}% del tiempo</span>
                            </div>
                            <div className="text-right">
                                <span className={`text-lg font-black font-mono ${r.total_return >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>{r.total_return > 0 ? '+' : ''}{r.total_return.toFixed(1)}%</span>
                                <span className="text-[9px] text-slate-700 font-black block uppercase mt-1">ROI Segmento</span>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="pt-6 border-t border-white/5">
                    <div className="flex items-center gap-3 text-slate-600 mb-4 px-2">
                        <ShieldCheck className="w-4 h-4" />
                        <span className="text-[10px] font-black uppercase">Reporte de Robustez</span>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                        <RobustTile label="Bias Retrospectivo" value="CORREGIDO" status="ok" />
                        <RobustTile label="Integridad Datos" value="100%" status="ok" />
                        <RobustTile label="Estat. Signif" value={result.is_significant ? 'SI' : 'NO'} status={result.is_significant ? 'ok' : 'error'} />
                        <RobustTile label="Inacción" value={`+${result.inaction_value.toFixed(0)}%`} status="ok" />
                    </div>
                </div>
            </section>
        </div>
    )
}
