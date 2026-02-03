
import { Microscope, Sparkles } from 'lucide-react'

interface HeaderProps {
    guidedMode: boolean
    setGuidedMode: (mode: boolean) => void
}

export function Header({ guidedMode, setGuidedMode }: HeaderProps) {
    return (
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-8 bg-slate-900/40 p-8 rounded-[2.5rem] border border-white/5 backdrop-blur-3xl shadow-2xl">
            <div className="flex items-center gap-6">
                <div className="w-16 h-16 bg-gradient-to-tr from-emerald-400 to-cyan-500 rounded-3xl flex items-center justify-center shadow-2xl shadow-emerald-500/20 group hover:scale-105 transition-transform cursor-pointer">
                    <Microscope className="text-slate-900 w-8 h-8 group-hover:rotate-12 transition-transform" />
                </div>
                <div>
                    <h1 className="text-3xl font-black text-white tracking-tighter flex items-center gap-3">
                        QUANT <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">DISCOVERY</span>
                        <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full text-[10px] font-black text-emerald-400 tracking-widest uppercase">Lab Edition</span>
                    </h1>
                    <p className="text-xs text-slate-500 font-bold uppercase tracking-[0.3em] mt-1.5 opacity-80">Laboratorio de exploración algorítmica honesta</p>
                </div>
            </div>

            <div className="flex items-center gap-4 bg-slate-950/50 p-2 rounded-2xl border border-white/5">
                <button
                    onClick={() => setGuidedMode(!guidedMode)}
                    className={`flex items-center gap-2 px-6 py-2.5 rounded-xl text-xs font-black transition-all ${guidedMode ? 'bg-emerald-500 text-slate-950 shadow-lg shadow-emerald-500/20' : 'text-slate-500 hover:text-slate-300'}`}
                >
                    <Sparkles className="w-4 h-4" />
                    MODO GUIADO {guidedMode ? 'ACTIVO' : 'INACTIVO'}
                </button>
            </div>
        </header>
    )
}
