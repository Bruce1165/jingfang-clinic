'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'

export default function Dashboard() {
  const [patients, setPatients] = useState(0)
  const [formulas, setFormulas] = useState(0)
  const [apiOk, setApiOk] = useState(false)

  useEffect(() => {
    fetch('/api/health').then(r => r.ok && setApiOk(true)).catch(() => {})
    fetch('/api/patients/').then(r => r.json()).then(d => setPatients(d.total || 0)).catch(() => {})
    fetch('/api/prescriptions/classics/').then(r => r.json()).then(d => setFormulas(Array.isArray(d) ? d.length : 0)).catch(() => {})
  }, [])

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-amber-900">欢迎</h1>
        <p className="text-stone-400 mt-1">今日 {new Date().toLocaleDateString('zh-CN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {[
          { label: '在籍患者', value: patients, link: '/patients', btn: '查看全部' },
          { label: '经典方剂', value: formulas, link: '/formulas', btn: '浏览方剂' },
          { label: 'API 状态', value: apiOk ? '正常' : '未连接', link: null, btn: null },
        ].map((s, i) => (
          <div key={i} className="card text-center">
            <div className="text-4xl font-bold text-amber-700 mt-2">{s.value}</div>
            <div className="text-stone-500 mt-1">{s.label}</div>
            {s.link && <Link href={s.link} className="btn-secondary mt-4 inline-block text-sm">{s.btn}</Link>}
          </div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="font-semibold text-amber-900 mb-4">快速操作</h2>
          <div className="space-y-2">
            {[
              { href: '/patients/new', icon: '👤', title: '新建患者档案', desc: '录入基础信息与生辰八字' },
              { href: '/formulas', icon: '📜', title: '查阅经典方剂', desc: '伤寒论·金匮要略方剂库（12方）' },
            ].map((item, i) => (
              <Link key={i} href={item.href} className="flex items-center gap-3 p-3 rounded-lg hover:bg-amber-50 transition-colors">
                <span className="text-2xl">{item.icon}</span>
                <div>
                  <div className="font-medium text-stone-800">{item.title}</div>
                  <div className="text-sm text-stone-400">{item.desc}</div>
                </div>
              </Link>
            ))}
          </div>
        </div>
        <div className="card">
          <h2 className="font-semibold text-amber-900 mb-4">系统说明</h2>
          <ul className="text-sm text-stone-600 space-y-2">
            <li>✅ 患者档案管理（含生辰八字）</li>
            <li>✅ 就诊记录（舌诊、辨证、六经）</li>
            <li>✅ 处方开具（经方选择+加减）</li>
            <li>✅ 处方打印（药房版/患者版）</li>
            <li>⏳ 疗效统计分析（开发中）</li>
            <li>⏳ AI 辅助辨证（下一版）</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
