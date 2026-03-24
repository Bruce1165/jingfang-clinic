'use client'
import { useEffect, useState } from 'react'

interface Formula { id: string; name: string; source: string; syndrome: string; indication: string }
interface FormulaDetail extends Formula {
  cooking_notes: string
  herbs: { herb_name: string; dosage_liang?: number; dosage_g?: number; processing?: string; notes?: string }[]
}

export default function FormulasPage() {
  const [formulas, setFormulas] = useState<Formula[]>([])
  const [search, setSearch] = useState('')
  const [sel, setSel] = useState<FormulaDetail | null>(null)

  useEffect(() => {
    fetch('/api/prescriptions/classics/').then(r => r.json()).then(setFormulas)
  }, [])

  const pick = async (f: Formula) => {
    const d = await fetch(`/api/prescriptions/classics/${f.id}`).then(r => r.json())
    setSel(d)
  }

  const filtered = formulas.filter(f => !search || f.name.includes(search) || (f.syndrome||'').includes(search) || (f.indication||'').includes(search))

  return (
    <div className="space-y-5">
      <h1 className="text-2xl font-bold text-stone-900">经典方剂库</h1>
      <input className="input max-w-xs" placeholder="搜索方名、主治..." value={search} onChange={e => setSearch(e.target.value)} />

      <div className="grid md:grid-cols-5 gap-6">
        <div className="md:col-span-2 space-y-2">
          {filtered.map(f => (
            <button key={f.id} onClick={() => pick(f)}
              className={`w-full text-left p-3 rounded-xl border transition-all ${sel?.id===f.id?'border-amber-500 bg-amber-50':'border-stone-200 bg-white hover:border-amber-300'}`}>
              <div className="font-semibold text-stone-900">{f.name}</div>
              <div className="text-xs text-amber-600">《{f.source}》</div>
              <div className="text-sm text-stone-500 mt-0.5 line-clamp-2">{f.syndrome}</div>
            </button>
          ))}
        </div>

        <div className="md:col-span-3">
          {sel ? (
            <div className="card sticky top-6 space-y-4">
              <div>
                <div className="text-xl font-bold text-amber-900">{sel.name}</div>
                <div className="text-sm text-amber-600">《{sel.source}》</div>
              </div>
              {sel.syndrome && <div><div className="label">主治证候</div><p className="text-sm">{sel.syndrome}</p></div>}
              {sel.indication && <div><div className="label">治法</div><p className="text-sm">{sel.indication}</p></div>}
              <div>
                <div className="label">药味组成（{sel.herbs.length}味）</div>
                <div className="flex flex-wrap gap-1.5 mt-1">
                  {sel.herbs.map((h, i) => (
                    <span key={i} className="bg-amber-50 border border-amber-200 rounded px-2 py-1 text-sm">
                      <b>{h.herb_name}</b>
                      {h.dosage_liang && <span className="text-stone-400 ml-1">{h.dosage_liang}两/{h.dosage_g}g</span>}
                      {h.processing && <span className="text-xs text-stone-400 ml-1">（{h.processing}）</span>}
                      {h.notes && <span className="text-xs text-stone-400 ml-1">{h.notes}</span>}
                    </span>
                  ))}
                </div>
              </div>
              {sel.cooking_notes && (
                <div><div className="label">经典煎法</div><p className="text-xs text-stone-500 leading-relaxed">{sel.cooking_notes}</p></div>
              )}
            </div>
          ) : (
            <div className="card text-center py-16 text-stone-400">← 点击左侧方剂查看详情</div>
          )}
        </div>
      </div>
    </div>
  )
}
