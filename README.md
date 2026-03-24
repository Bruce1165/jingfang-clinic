# 经方诊所管理系统 v0.1

基于倪海厦经方体系的中医诊所管理系统。

## 环境要求

- Python 3.9+
- Node.js 18+
- 无需 Docker

## 快速启动

```bash
# 赋权并启动（自动安装依赖、初始化数据库、启动前后端）
chmod +x start.sh
./start.sh
```

启动后访问：
- 前端：http://localhost:3000
- API文档：http://localhost:8000/docs

## 目录结构

```
jingfang-clinic/
├── backend/                  # FastAPI 后端
│   ├── main.py               # 入口
│   ├── core/
│   │   ├── config.py         # 配置（SQLite路径、密钥等）
│   │   └── database.py       # 数据库连接
│   ├── api/
│   │   ├── models/           # SQLAlchemy 模型
│   │   ├── routers/          # API 路由
│   │   └── schemas/          # Pydantic 数据校验
│   ├── scripts/
│   │   └── seed_formulas.py  # 初始化12个经典方剂
│   └── requirements.txt
├── frontend/                 # Next.js 前端
│   └── app/
│       ├── page.tsx          # 首页仪表盘
│       ├── patients/         # 患者管理
│       ├── visits/           # 就诊记录
│       └── formulas/         # 经方库
├── start.sh                  # 一键启动脚本
└── README.md
```

## 已实现功能

| 功能 | 状态 |
|------|------|
| 患者档案管理 | ✅ |
| 生辰八字录入 | ✅ |
| 就诊记录（舌诊/辨证/六经）| ✅ |
| 处方开具（选经方+加减）| ✅ |
| 处方打印（药房版/患者版）| ✅ |
| 12个经典方剂预置 | ✅ |
| 疗效跟踪 | ✅ |
| AI辨证建议 | 🔜 下一版 |
| 八字自动推算 | 🔜 下一版 |
| 统计分析 | 🔜 下一版 |

## 数据库

开发环境使用 SQLite（文件：`backend/jingfang.db`）。
生产环境可替换为 PostgreSQL，修改 `backend/.env` 中的 `DATABASE_URL` 即可。

## 预置经典方剂（12方）

桂枝汤、麻黄汤、小柴胡汤、四逆汤、酸枣仁汤、大承气汤、
真武汤、炙甘草汤、理中丸、黄连阿胶汤、当归四逆汤、乌梅丸
