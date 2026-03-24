import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '经方诊所管理系统',
  description: '基于倪海厦经方体系的中医诊所管理系统',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>
        <div className="min-h-screen flex flex-col">
          <header className="bg-amber-800 text-white px-6 py-4 shadow-md">
            <div className="max-w-5xl mx-auto flex items-center gap-4">
              <span className="text-2xl">🌿</span>
              <div>
                <div className="text-lg font-bold">经方诊所管理系统</div>
                <div className="text-amber-200 text-xs">倪海厦经方体系 · 经方临床管理</div>
              </div>
              <nav className="ml-auto flex gap-6 text-sm">
                <a href="/" className="hover:text-amber-200 transition-colors">首页</a>
                <a href="/patients" className="hover:text-amber-200 transition-colors">患者</a>
                <a href="/patients/new" className="hover:text-amber-200 transition-colors">+ 新患者</a>
                <a href="/formulas" className="hover:text-amber-200 transition-colors">经方库</a>
              </nav>
            </div>
          </header>
          <main className="flex-1 max-w-5xl mx-auto w-full px-6 py-8">
            {children}
          </main>
          <footer className="text-center text-stone-400 text-xs py-4 border-t">
            经方诊所管理系统 v0.1 · 仅供临床医师使用
          </footer>
        </div>
      </body>
    </html>
  )
}
