from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.database import engine, Base
from api.routers import patients, visits, prescriptions

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时自动建表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # 初始化经典方剂
    try:
        from scripts.seed_formulas import seed
        await seed()
    except Exception as e:
        print(f"Seed warning: {e}")
    yield

app = FastAPI(
    title="经方诊所管理系统",
    description="基于经方（倪海厦体系）的中医诊所管理系统",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router)
app.include_router(visits.router)
app.include_router(prescriptions.router)

@app.get("/", tags=["系统"])
async def root():
    return {"status": "ok", "message": "经方诊所管理系统 API", "docs": "/docs"}

@app.get("/health", tags=["系统"])
async def health():
    return {"status": "healthy"}
