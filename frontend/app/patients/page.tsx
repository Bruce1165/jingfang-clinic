'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'

interface Patient {
  id: string; name: string; gender: string; age?: number; phone?: string;
  bazi_year?: string; bazi_month?: string; bazi_day?: string; bazi_hour?: string;
  constitution_hint?: string; visit_count: number;
}

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    const url = search ? `/api/patients/?search=${encodeURIComponent(search)}` : '/api/patients/'
    fetch(url).then(r => r.json()).then(d => { setPatients(d.patients || []); setLoading(false) })
  }, [search])

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-stone-900">患者档案</h1>
        <Link href="/patients/new" className="btn-primary">+ 新建患者</Link>
      </div>
      <input className="input max-w-xs" placeholder="搜索姓名/电话..." value={search} onChange={e => setSearch(e.target.value)} />

      {loading ? <div className="text-center py-16 text-stone-400">加载中...</div> : patients.length === 0 ? (
        <div className="card text-center py-16">
          <p className="text-stone-400 text-lg mb-4">暂无患者</p>
          <Link href="/patients/new" className="btn-primary">立即新建</Link>
        </div>
      ) : (
        <div className="space-y-3">
          {patients.map(p => (
            <Link key={p.id} href={`/patients/${p.id}`} className="card block hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start">
                <div className="flex gap-4 items-center">
                  <div className="w-11 h-11 rounded-full bg-amber-100 flex items-center justify-center text-xl">
                    {p.gender === 'male' ? '👨' : '👩'}
                  </div>
                  <div>
                    <div className="font-semibold text-stone-900 text-lg">{p.name}</div>
                    <div className="text-sm text-stone-400 space-x-2">
                      {p.age && <span>{p.age}岁</span>}
                      {p.phone && <span>📱 {p.phone}</span>}
                    </div>
                    {(p.bazi_year || p.constitution_hint) && (
                      <div className="text-xs text-amber-700 mt-0.5">
                        {p.bazi_year && `八字：${p.bazi_year}${p.bazi_month}${p.bazi_day}${p.bazi_hour}`}
                        {p.constitution_hint && ` · ${p.constitution_hint}`}
                      </div>
                    )}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-amber-700">{p.visit_count}</div>
                  <div className="text-xs text-stone-400">就诊</div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
