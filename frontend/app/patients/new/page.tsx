'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'

const HOURS = ['子(23-1)','丑(1-3)','寅(3-5)','卯(5-7)','辰(7-9)','巳(9-11)',
  '午(11-13)','未(13-15)','申(15-17)','酉(17-19)','戌(19-21)','亥(21-23)']

export default function NewPatientPage() {
  const router = useRouter()
  const [f, setF] = useState({ name:'', gender:'male', birth_date:'', age:'', phone:'', address:'', birth_hour_raw:'', constitution_hint:'', notes:'' })
  const [saving, setSaving] = useState(false)
  const [err, setErr] = useState('')
  const set = (k: string, v: string) => setF(prev => ({...prev, [k]: v}))

  const submit = async (e: React.FormEvent) => {
    e.preventDefault(); setSaving(true); setErr('')
    try {
      const body: Record<string, unknown> = { name: f.name, gender: f.gender }
      if (f.birth_date) body.birth_date = f.birth_date
      if (f.age) body.age = parseInt(f.age)
      if (f.phone) body.phone = f.phone
      if (f.address) body.address = f.address
      if (f.birth_hour_raw) body.birth_hour_raw = f.birth_hour_raw
      if (f.constitution_hint) body.constitution_hint = f.constitution_hint
      if (f.notes) body.notes = f.notes

      const res = await fetch('/api/patients/', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(body) })
      if (!res.ok) { const d = await res.json(); throw new Error(d.detail || '保存失败') }
      const data = await res.json()
      router.push(`/patients/${data.id}`)
    } catch (e: unknown) { setErr(e instanceof Error ? e.message : '保存失败'); setSaving(false) }
  }

  return (
    <div className="max-w-xl space-y-6">
      <div className="flex items-center gap-3">
        <button onClick={() => router.back()} className="text-stone-400 hover:text-stone-600 text-sm">← 返回</button>
        <h1 className="text-2xl font-bold text-stone-900">新建患者</h1>
      </div>

      <form onSubmit={submit} className="space-y-5">
        <div className="card space-y-4">
          <div className="text-sm font-semibold text-amber-800 border-b border-amber-100 pb-2">基础信息</div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="label">姓名 *</label><input required className="input" value={f.name} onChange={e => set('name', e.target.value)} /></div>
            <div><label className="label">性别 *</label>
              <select className="input" value={f.gender} onChange={e => set('gender', e.target.value)}>
                <option value="male">男</option><option value="female">女</option>
              </select>
            </div>
            <div><label className="label">出生日期</label><input type="date" className="input" value={f.birth_date} onChange={e => set('birth_date', e.target.value)} /></div>
            <div><label className="label">年龄（岁）</label><input type="number" className="input" value={f.age} onChange={e => set('age', e.target.value)} /></div>
            <div><label className="label">手机</label><input className="input" value={f.phone} onChange={e => set('phone', e.target.value)} /></div>
            <div><label className="label">地址</label><input className="input" value={f.address} onChange={e => set('address', e.target.value)} /></div>
          </div>
        </div>

        <div className="card space-y-4">
          <div className="text-sm font-semibold text-amber-800 border-b border-amber-100 pb-2">生辰八字</div>
          <div className="bg-amber-50 rounded-lg p-3 text-xs text-amber-700">
            💡 填写出生日期后可自动推算八字。出生时辰影响时柱，请尽量准确填写。
          </div>
          <div><label className="label">出生时辰</label>
            <select className="input" value={f.birth_hour_raw} onChange={e => set('birth_hour_raw', e.target.value)}>
              <option value="">-- 不确定 --</option>
              {HOURS.map(h => <option key={h} value={h.slice(0,1)}>{h}</option>)}
            </select>
          </div>
          <div><label className="label">体质倾向</label>
            <input className="input" placeholder="如：阳虚体质 / 肝郁气滞..." value={f.constitution_hint} onChange={e => set('constitution_hint', e.target.value)} />
          </div>
        </div>

        <div className="card">
          <label className="label">备注</label>
          <textarea className="input h-20 resize-none" value={f.notes} onChange={e => set('notes', e.target.value)} />
        </div>

        {err && <div className="bg-red-50 text-red-600 text-sm rounded-lg p-3">{err}</div>}

        <div className="flex gap-3">
          <button type="submit" disabled={saving} className="btn-primary flex-1">{saving ? '保存中...' : '✓ 保存'}</button>
          <button type="button" onClick={() => router.back()} className="btn-secondary">取消</button>
        </div>
      </form>
    </div>
  )
}
