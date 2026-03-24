#!/bin/bash
# 经方诊所管理系统 - 一键启动脚本（无需Docker）
set -e

echo "🌿 经方诊所管理系统启动中..."
echo ""

# 检查Python
if ! command -v python3 &>/dev/null; then echo "❌ 未找到 python3"; exit 1; fi
echo "✅ Python: $(python3 --version)"

# 检查Node
if ! command -v node &>/dev/null; then echo "❌ 未找到 node"; exit 1; fi
echo "✅ Node: $(node --version)"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# === 后端 ===
echo ""
echo "📦 安装后端依赖..."
cd "$SCRIPT_DIR/backend"
pip3 install -r requirements.txt -q

echo "🗄  初始化数据库（SQLite）..."
python3 -c "
import asyncio, sys, os
sys.path.insert(0, '.')
from core.database import engine, Base
from api.models.patient import Patient
from api.models.visit import Visit
from api.models.prescription import Prescription, PrescriptionHerb, ClassicFormula, ClassicFormulaHerb
async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('  数据库表已创建')
asyncio.run(init())
"

python3 scripts/seed_formulas.py

echo "🚀 启动后端 API (端口 8000)..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "  后端 PID: $BACKEND_PID"

# 等待后端就绪
echo "  等待后端启动..."
for i in {1..15}; do
  if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "  ✅ 后端已就绪"
    break
  fi
  sleep 1
done

# === 前端 ===
echo ""
echo "📦 安装前端依赖..."
cd "$SCRIPT_DIR/frontend"
npm install --silent

echo "🚀 启动前端 (端口 3000)..."
npm run dev &
FRONTEND_PID=$!
echo "  前端 PID: $FRONTEND_PID"

echo ""
echo "════════════════════════════════════════"
echo "  🌿 经方诊所管理系统 已启动"
echo ""
echo "  前端界面: http://localhost:3000"
echo "  API 文档: http://localhost:8000/docs"
echo ""
echo "  按 Ctrl+C 停止所有服务"
echo "════════════════════════════════════════"

# 等待并捕获退出
trap "echo ''; echo '停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
