

export function NiceSelect({ label, description, value, onChange, options }: any) {
    return (
        <div className="space-y-2.5">
            <label className="text-[11px] font-black text-slate-600 uppercase mb-2 block tracking-widest">{label}</label>
            <select
                value={value}
                onChange={e => onChange(e.target.value)}
                className="w-full bg-slate-950 border-2 border-white/5 hover:border-white/10 transition-all rounded-[1.25rem] px-5 py-4 text-sm font-bold text-slate-300 outline-none appearance-none cursor-pointer"
            >
                {options?.map((opt: any) => (
                    <option key={opt.value || opt} value={opt.value || opt}>{opt.label || opt}</option>
                ))}
            </select>
            {description && <p className="text-[10px] text-slate-600 italic px-1">{description}</p>}
        </div>
    )
}
