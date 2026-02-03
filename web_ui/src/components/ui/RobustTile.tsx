

export function RobustTile({ label, value, status }: any) {
    return (
        <div className="bg-slate-900 border border-white/5 p-4 rounded-2xl flex flex-col items-center justify-center text-center">
            <span className="text-[8px] font-black text-slate-700 uppercase mb-1 tracking-widest">{label}</span>
            <div className={`text-[10px] font-black font-mono rounded-lg px-2 py-0.5 ${status === 'ok' ? 'text-emerald-500' : 'text-rose-500'}`}>
                {value}
            </div>
        </div>
    )
}
