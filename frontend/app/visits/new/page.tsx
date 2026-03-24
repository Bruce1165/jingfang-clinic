'use client'
import { useState, useEffect, Suspense } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'

interface Formula { id: string; name: string; syndrome: string }
interface Herb { herb_name: string; dosage_g: number; processing: string }

const SIX_CH = ['太阳病','阳明病','少阳病','太阴病','少阴病','厥阴病','合病']
const TONGUE_C = ['淡白','淡红','红','绛','紫']
const TONGUE_CO = ['白苔','黄苔','灰黑苔','无苔']
const COATING_T = ['薄','厚','腻','燥','剥']

function NewVisitInner() {
  const router = useRouter()
  const params = useSearchParams()
  const patient_id = params.get('patient_id') || ''

  const [step, setStep] = useState(1)
  const [visitId, setVisitId] = useState('')
  const [saving, setSaving] = useState(false)
  const [err, setErr] = useState('')

  // 症状
  const [chief, setChief] = useState('')
  const [inquiry, setInquiry] = useState('')
  const [tColor, setTColor] = useState('')
  const [tCoating, setTCoating] = useState('')
  const [tTexture, setTTexture] = useState('')
  const [sixCh, setSixCh] = useState('')
  const [coldHeat, setColdHeat] = useState('')
  const [xuShi, setXuShi] = useState('')
  const [docNotes, setDocNotes] = useState('')
  const [days, setDays] = useState(7)

  // 处方
  const [allFormulas, setAllFormulas] = useState<Formula[]>([])
  const [fSearch, setFSearch] = useState('')
  const [selFormula, setSelFormula] = useState<{id:string;name:string;cooking_notes?:string} | null>(null)
  const [herbs, setHerbs] = useState<Herb[]>([])
  const [modNotes, setModNotes] = useState('')
  const [cooking, setCooking] = useState('')
  const [patNote, setPatNote] = useState('')

  useEffect(() => {
    fetch('/api/prescriptions/classics/').then(r => r.json()).then(setAllFormulas)
  }, [])

  const filtered = allFormulas.filter(f => !fSearch || f.name.includes(fSearch) || (f.syndrome||'').includes(fSearch))

  const pickFormula = async (f: Formula) => {
    const d = await fetch(`/api/prescriptions/classics/${f.id}`).then(r => r.json())
    setSelFormula(d)
    setHerbs((d.herbs || []).map((h: {herb_name:string;dosage_g?:number;processing?:string}) => ({
      herb_name: h.herb_name, dosage_g: h.dosage_g || 10, processing: h.processing || ''
    })))
    setCooking(d.cooking_notes || '')
  }

  const saveStep1 = async () => {
    if (!chief.trim()) { setErr('请填写主诉'); return }
    setSaving(true); setErr('')
    try {
      const res = await fetch('/api/visits/', { method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ patient_id, chief_complaint: chief, inquiry_notes: inquiry,
          tongue_color: tColor, tongue_coating: tCoating, tongue_coating_texture: tTexture,
          syndrome_cold_heat: coldHeat, syndrome_xu_shi: xuShi, six_channel: sixCh,
          doctor_notes: docNotes, days_of_medicine: days }) })
      if (!res.ok) throw new Error('保存失败')
      const d = await res.json()
      setVisitId(d.id); setStep(2)
    } catch(e: unknown) { setErr(e instanceof Error ? e.message : '失败') }
    setSaving(false)
  }

  const saveRx = async () => {
    setSaving(true); setErr('')
    try {
      const res = await fetch('/api/prescriptions/', { method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ visit_id: visitId, classic_formula_name: selFormula?.name,
          modification_notes: modNotes, cooking_instructions: cooking,
          doses: days, patient_notes: patNote, herbs }) })
      if (!res.ok) throw new Error('保存处方失败')
      router.push(`/visits/${visitId}`)
    } catch(e: unknown) { setErr(e instanceof Error ? e.message : '失败') }
    setSaving(false)
  }

  return (
    <div className="max-w-2xl space-y-5">
      <div className="flex items-center gap-3">
        <button onClick={() => router.back()} className="text-stone-400 hover:text-stone-600 text-sm">← 返回</button>
        <h1 className="text-2xl font-bold text-stone-900">新建就诊记录</h1>
      </div>

      <div className="flex gap-2 text-sm">
        {['1. 症状辨析','2. 处方开具'].map((l, i) => (
          <div key={i} className={`px-4 py-2 rounded-lg font-medium ${step===i+1?'bg-amber-700 text-white':'bg-stone-100 text-stone-400'}`}>{l}</div>
        ))}
      </div>

      {step === 1 && (
        <div className="space-y-4">
          <div className="card space-y-4">
            <div className="font-semibold text-amber-800 text-sm border-b pb-2">主诉与问诊</div>
            <div><label className="label">主诉 *</label>
              <textarea className="input h-20 resize-none" placeholder="患者主要症状与就诊原因..." value={chief} onChange={e => setChief(e.target.value)} /></div>
            <div><label className="label">问诊备注（睡眠、饮食、二便等）</label>
              <textarea className="input h-20 resize-none" value={inquiry} onChange={e => setInquiry(e.target.value)} /></div>
          </div>

          <div className="card space-y-4">
            <div className="font-semibold text-amber-800 text-sm border-b pb-2">舌诊</div>
            <div className="grid grid-cols-3 gap-3">
              {[['舌色', TONGUE_C, tColor, setTColor],['苔色', TONGUE_CO, tCoating, setTCoating],['苔质', COATING_T, tTexture, setTTexture]].map(([label, opts, val, setter], i) => (
                <div key={i}><label className="label">{label as string}</label>
                  <select className="input" value={val as string} onChange={e => (setter as (v:string)=>void)(e.target.value)}>
                    <option value="">-</option>{(opts as string[]).map(o => <option key={o}>{o}</option>)}
                  </select>
                </div>
              ))}
            </div>
          </div>

          <div className="card space-y-4">
            <div className="font-semibold text-amber-800 text-sm border-b pb-2">辨证</div>
            <div className="grid grid-cols-3 gap-3">
              <div><label className="label">寒热</label>
                <select className="input" value={coldHeat} onChange={e => setColdHeat(e.target.value)}>
                  <option value="">-</option>{['寒','热','寒热错杂'].map(o => <option key={o}>{o}</option>)}
                </select>
              </div>
              <div><label className="label">虚实</label>
                <select className="input" value={xuShi} onChange={e => setXuShi(e.target.value)}>
                  <option value="">-</option>{['虚','实','虚实夹杂'].map(o => <option key={o}>{o}</option>)}
                </select>
              </div>
              <div><label className="label">六经</label>
                <select className="input" value={sixCh} onChange={e => setSixCh(e.target.value)}>
                  <option value="">-</option>{SIX_CH.map(o => <option key={o}>{o}</option>)}
                </select>
              </div>
            </div>
            <div><label className="label">医师辨析</label>
              <textarea className="input h-16 resize-none text-sm" placeholder="辨证分析、治则..." value={docNotes} onChange={e => setDocNotes(e.target.value)} /></div>
          </div>

          <div className="card">
            <label className="label">开药天数</label>
            <div className="flex gap-2 mt-1">
              {[3,5,7,10,14].map(d => (
                <button key={d} onClick={() => setDays(d)} className={`px-3 py-1.5 rounded-lg border text-sm ${days===d?'bg-amber-700 text-white border-amber-700':'border-stone-200 hover:border-amber-400'}`}>{d}天</button>
              ))}
            </div>
          </div>

          {err && <div className="bg-red-50 text-red-600 text-sm rounded-lg p-3">{err}</div>}
          <button onClick={saveStep1} disabled={saving} className="btn-primary w-full">{saving ? '保存中...' : '下一步：开处方 →'}</button>
        </div>
      )}

      {step === 2 && (
        <div className="space-y-4">
          <div className="card space-y-3">
            <div className="font-semibold text-amber-800 text-sm border-b pb-2">选择基础方</div>
            <input className="input" placeholder="搜索方名或证候..." value={fSearch} onChange={e => setFSearch(e.target.value)} />
            <div className="grid grid-cols-2 gap-2 max-h-44 overflow-y-auto pr-1">
              {filtered.map(f => (
                <button key={f.id} onClick={() => pickFormula(f)}
                  className={`text-left p-3 rounded-lg border text-sm transition-colors ${selFormula?.id===f.id?'border-amber-500 bg-amber-50':'border-stone-200 hover:border-amber-300'}`}>
                  <div className="font-medium">{f.name}</div>
                  <div className="text-xs text-stone-400 mt-0.5 line-clamp-1">{f.syndrome}</div>
                </button>
              ))}
            </div>
          </div>

          {herbs.length > 0 && (
            <div className="card space-y-3">
              <div className="font-semibold text-amber-800 text-sm border-b pb-2">
                药味调整 <span className="text-stone-400 font-normal">（1两 = 5克）</span>
              </div>
              {herbs.map((h, i) => (
                <div key={i} className="flex items-center gap-2">
                  <input className="input w-24 text-sm font-medium" value={h.herb_name} onChange={e => { const nh=[...herbs]; nh[i].herb_name=e.target.value; setHerbs(nh) }} />
                  <input type="number" className="input w-16 text-sm" value={h.dosage_g} min={1}
                    onChange={e => { const nh=[...herbs]; nh[i].dosage_g=parseFloat(e.target.value)||0; setHerbs(nh) }} />
                  <span className="text-xs text-stone-400 whitespace-nowrap">{(h.dosage_g/5).toFixed(1)}两</span>
                  <input className="input flex-1 text-sm" placeholder="炮制..." value={h.processing}
                    onChange={e => { const nh=[...herbs]; nh[i].processing=e.target.value; setHerbs(nh) }} />
                  <button onClick={() => setHerbs(herbs.filter((_,j)=>j!==i))} className="text-red-400 hover:text-red-600 text-xl px-1">×</button>
                </div>
              ))}
              <button onClick={() => setHerbs([...herbs,{herb_name:'',dosage_g:10,processing:''}])} className="text-sm text-amber-700 hover:underline">+ 加药</button>
            </div>
          )}

          <div className="card space-y-3">
            <div className="font-semibold text-amber-800 text-sm border-b pb-2">处方说明</div>
            <div><label className="label">加减说明</label><textarea className="input h-14 resize-none text-sm" value={modNotes} onChange={e => setModNotes(e.target.value)} /></div>
            <div><label className="label">煎服法</label><textarea className="input h-14 resize-none text-sm" value={cooking} onChange={e => setCooking(e.target.value)} /></div>
            <div><label className="label">给患者的说明</label><textarea className="input h-14 resize-none text-sm" value={patNote} onChange={e => setPatNote(e.target.value)} /></div>
          </div>

          {err && <div className="bg-red-50 text-red-600 text-sm rounded-lg p-3">{err}</div>}
          <div className="flex gap-3">
            <button onClick={saveRx} disabled={saving} className="btn-primary flex-1">{saving ? '保存中...' : '✓ 保存处方'}</button>
            <button onClick={() => router.push(`/visits/${visitId}`)} className="btn-secondary">跳过</button>
          </div>
        </div>
      )}
    </div>
  )
}

export default function NewVisitPage() {
  return <Suspense><NewVisitInner /></Suspense>
}
