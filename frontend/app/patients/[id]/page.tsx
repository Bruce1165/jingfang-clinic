'use client'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'

interface Visit { id: string; visit_number: number; visit_date: string; chief_complaint: string; six_channel: string; efficacy: string; next_visit_date: string }
interface Patient { id: string; name: string; gender: string; age?: number; phone?: string; bazi_year?: string; bazi_month?: string; bazi_day?: string; bazi_hour?: string; birth_hour_raw?: string; constitution_hint?: string; notes?: string; visit_count: number }

const EFFICACY: Record<string, string> = { improved: '✅ 好转', unchanged: '➡️ 未变', worsened: '⚠️ 加重', first_visit: '初诊' }

export default function PatientDetail() {
  const { id } = useParams() as { id: string }
  const [patient, setPatient] = useState<Patient | null>(null)
  const [visits, setVisits] = useState<Visit[]>([])

  useEffect(() => {
    fetch(`/api/patients/${id}`).then(r => r.json()).then(setPatient)
    fetch(`/api/visits/patient/${id}`).then(r => r.json()).then(setVisits)
  }, [id])

  if (!patient) return <div className="text-center py-16 text-stone-400">加载中...</div>

  return (
    <div className="max-w-3xl space-y-6">
      <Link href="/patients" className="text-stone-400 hover:text-stone-600 text-sm">← 患者列表</Link>

      <div className="card">
        <div className="flex justify-between items-start">
          <div className="flex gap-4 items-center">
            <div className="w-14 h-14 rounded-full bg-amber-100 flex items-center justify-center text-3xl">
              {patient.gender === 'male' ? '👨' : '👩'}
            </div>
            <div>
              <div className="text-2xl font-bold text-stone-900">{patient.name}</div>
              <div className="text-stone-500 text-sm">
                {patient.age && `${patient.age}岁 · `}{patient.phone || '无电话'}
              </div>
              {patient.bazi_year && (
                <div className="text-sm text-amber-700 mt-1">
                  八字：{patient.bazi_year} {patient.bazi_month} {patient.bazi_day} {patient.bazi_hour}
                  {patient.birth_hour_raw && ` · ${patient.birth_hour_raw}时`}
                </div>
              )}
              {patient.constitution_hint && <div className="text-sm text-stone-600">体质：{patient.constitution_hint}</div>}
            </div>
          </div>
          <Link href={`/visits/new?patient_id=${id}`} className="btn-primary text-sm">+ 新建就诊</Link>
        </div>
        {patient.notes && <div className="mt-4 bg-stone-50 rounded-lg p-3 text-sm text-stone-600">{patient.notes}</div>}
      </div>

      <div>
        <div className="text-lg font-semibold text-stone-800 mb-3">就诊记录（{visits.length}次）</div>
        {visits.length === 0 ? (
          <div className="card text-center py-10 text-stone-400">
            <p>暂无就诊记录</p>
            <Link href={`/visits/new?patient_id=${id}`} className="btn-primary mt-3 inline-block text-sm">新建首诊</Link>
          </div>
        ) : (
          <div className="space-y-3">
            {visits.map(v => (
              <Link key={v.id} href={`/visits/${v.id}`} className="card block hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start">
                  <div>
                    <div className="font-semibold">第{v.visit_number}诊 · {new Date(v.visit_date).toLocaleDateString('zh-CN')}</div>
                    <div className="text-stone-500 text-sm mt-1">{v.chief_complaint || '—'}</div>
                    {v.six_channel && <div className="text-xs text-amber-700 mt-1">{v.six_channel}</div>}
                  </div>
                  <div className="text-sm text-right">
                    <div>{EFFICACY[v.efficacy] || v.efficacy}</div>
                    {v.next_visit_date && <div className="text-stone-400 text-xs mt-1">复诊 {new Date(v.next_visit_date).toLocaleDateString('zh-CN')}</div>}
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
