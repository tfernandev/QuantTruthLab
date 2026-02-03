

export function DetailedMetric({ label, value, desc, info }: any) {
    return (
        <div className="flex-1 min-w-[120px] group relative">
            <p className="text-[10px] font-black text-slate-600 uppercase tracking-widest mb-1 group-hover:text-emerald-500 transition-colors">{label}</p>
            <p className="text-2xl font-black text-white font-mono tracking-tighter mb-1">{value}</p>
            <p className="text-[9px] text-slate-700 font-bold max-w-[100px] mx-auto leading-tight">{desc}</p>
            {info && (
                <div className="absolute -top-16 left-0 w-40 bg-zinc-900 p-2 rounded-lg text-[9px] font-bold text-slate-300 shadow-xl border border-white/5 opacity-0 group-hover:opacity-100 transition-opacity z-30 pointer-events-none">
                    {info}
                </div>
            )}
        </div>
    )
}
