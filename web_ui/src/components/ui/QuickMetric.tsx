

export function QuickMetric({ label, value, positive, neutral, tooltip }: any) {
    return (
        <div className="bg-slate-950 px-8 py-4 rounded-3xl border border-white/5 flex items-baseline gap-4 shadow-xl relative group">
            <span className="text-[10px] font-black text-slate-700 uppercase">{label}</span>
            <span className={`text-2xl font-black font-mono tracking-tighter ${neutral ? 'text-slate-400' : positive ? 'text-emerald-400' : 'text-rose-400'}`}>{value}</span>
            {tooltip && (
                <div className="absolute -top-14 left-0 w-48 bg-emerald-900 p-2 rounded-lg text-[9px] font-bold text-white shadow-xl border border-emerald-700 opacity-0 group-hover:opacity-100 transition-opacity z-30 pointer-events-none">
                    {tooltip}
                </div>
            )}
        </div>
    )
}
