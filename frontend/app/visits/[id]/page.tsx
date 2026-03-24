'use client'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'

const EFFICACY: Record<string, string> = { improved: '✅ 好转', unchanged: '➡️ 未变', worsened: '⚠️ 加重', first_visit: '初诊' }

export default function VisitDetail() {
  const { id } = useParams() as { id: string }
  const [visit, setVisit] = useState<Record<string, unknown> | null>(null)
  const [rxList, setRxList] = useState<Array<Record<string, unknown>>>([])
  const [printData, setPrintData] = useState<Record<string, unknown> | null>(null)

  useEffect(() => {
    fetch(`/api/visits/${id}`).then(r => r.json()).then(setVisit)
    fetch(`/api/prescriptions/visit/${id}`).then(r => r.json()).then(setRxList)
  }, [id])

  const handlePrint = async () => {
    try {
      const d = await fetch(`/api/prescriptions/visit/${id}/print`).then(r => r.json())
      setPrintData(d)
    } catch { alert('暂无处方') }
  }

  if (!visit) return <div className="text-center py-16 text-stone-400">加载中...</div>

  const pv = printData?.pharmacy_version as Record<string, unknown> | undefined

  return (
    <div className="max-w-2xl space-y-5">
      <Link href={`/patients/${visit.patient_id}`} className="text-stone-400 hover:text-stone-600 text-sm">← 返回患者</Link>

      <div className="card space-y-4">
        <div className="flex justify-between items-start">
          <div>
            <div className="text-xl font-bold">第{String(visit.visit_number)}诊</div>
            <div className="text-stone-400 text-sm">{new Date(visit.visit_date as string).toLocaleDateString('zh-CN')}</div>
          </div>
          <div className="text-sm">{EFFICACY[visit.efficacy as string] || visit.efficacy as string}</div>
        </div>

        {visit.chief_complaint && (
          <div><div className="label">主诉</div><p className="text-stone-700">{visit.chief_complaint as string}</p></div>
        )}
        {(visit.tongue_color || visit.tongue_coating) && (
          <div><div className="label">舌诊</div>
            <p className="text-stone-700">{[visit.tongue_color, visit.tongue_coating, visit.tongue_coating_texture].filter(Boolean).join(' · ')}</p>
          </div>
        )}
        {visit.six_channel && (
          <div><div className="label">六经辨证</div><p className="font-medium text-amber-700">{visit.six_channel as string}</p></div>
        )}
        {(visit.syndrome_cold_heat || visit.syndrome_xu_shi) && (
          <div className="flex gap-4 text-sm">
            {visit.syndrome_cold_heat && <span className="bg-blue-50 text-blue-700 px-2 py-1 rounded">{visit.syndrome_cold_heat as string}</span>}
            {visit.syndrome_xu_shi && <span className="bg-purple-50 text-purple-700 px-2 py-1 rounded">{visit.syndrome_xu_shi as string}</span>}
          </div>
        )}
        {visit.doctor_notes && (
          <div><div className="label">医师辨析</div><p className="text-stone-600 text-sm">{visit.doctor_notes as string}</p></div>
        )}
        {visit.inquiry_notes && (
          <div><div className="label">问诊记录</div><p className="text-stone-500 text-sm">{visit.inquiry_notes as string}</p></div>
        )}
        <div className="text-sm text-stone-400">复诊：{visit.next_visit_date ? new Date(visit.next_visit_date as string).toLocaleDateString('zh-CN') : '—'}</div>
      </div>

      {rxList.length > 0 && (
        <div className="card space-y-4">
          <div className="flex justify-between items-center">
            <div className="font-semibold text-amber-900">处方</div>
            <button onClick={handlePrint} className="btn-secondary text-sm">🖨 打印处方</button>
          </div>
          {rxList.map((rx, i) => (
            <div key={i} className="border border-amber-100 rounded-lg p-4 space-y-2">
              {rx.classic_formula_name && <div className="font-semibold text-amber-800">{rx.classic_formula_name as string}</div>}
              <div className="flex flex-wrap gap-1.5">
                {((rx.herbs || []) as Array<{herb_name:string;dosage_g:number;dosage_liang?:number;processing?:string}>).map((h, j) => (
                  <span key={j} className="bg-amber-50 border border-amber-200 rounded px-2 py-0.5 text-sm">
                    {h.herb_name} <b>{h.dosage_g}g</b>
                    {h.processing && <span className="text-xs text-stone-400 ml-1">{h.processing}</span>}
                  </span>
                ))}
              </div>
              {rx.cooking_instructions && <p className="text-xs text-stone-500">{rx.cooking_instructions as string}</p>}
              <p className="text-xs text-stone-400">共{rx.doses as number}剂</p>
            </div>
          ))}
        </div>
      )}

      {printData && pv && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-md w-full p-6 space-y-4">
            <div className="flex justify-between items-center">
              <div className="font-bold text-lg">{pv.formula_name as string}</div>
              <button onClick={() => setPrintData(null)} className="text-stone-400 hover:text-stone-600 text-2xl">×</button>
            </div>
            <div className="bg-stone-50 rounded-lg p-4 text-sm space-y-1 font-mono">
              {((pv.herbs || []) as string[]).map((h, i) => <div key={i}>{h}</div>)}
            </div>
            <div className="text-sm text-stone-600">{pv.cooking_instructions as string}</div>
            <div className="font-semibold text-amber-700">共{pv.doses as number}剂 · {pv.estimated_cost as string}</div>
            <button onClick={() => window.print()} className="btn-primary w-full">🖨 打印</button>
          </div>
        </div>
      )}
    </div>
  )
}
