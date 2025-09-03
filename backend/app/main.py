from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import characters, utils, ai
from app.services import gemini_service
from contextlib import asynccontextmanager

# --- 在应用启动时执行初始化 ---
# FastAPI 的事件处理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时执行的代码
    print("Application startup...")
    gemini_service.initialize_gemini()
    yield
    # 应用关闭时执行的代码 (如果有的话)
    print("Application shutdown...")

# 创建 FastAPI 应用实例
app = FastAPI(
    title="小说角色展示页 API",
    description="一个用于展示和管理小说角色信息的API。",
    version="0.1.0",
    # --- 新增/修改这三行 ---
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan # 注册 lifespan 事件处理器
)

# 定义允许的前端源列表
# 在开发阶段，我们通常允许本地开发服务器的地址
# Vue CLI 默认是 8080, Vite 默认是 5173。我们把常见的都加上。
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # 允许访问的源
    allow_credentials=True,         # 支持 cookie
    allow_methods=["*"],            # 允许所有方法 (GET, POST, PUT, DELETE 等)
    allow_headers=["*"],            # 允许所有请求头
)


@app.get("/", tags=["Root"])
def read_root():
    """
    根路径，用于简单的健康检查。
    """
    return {"message": "欢迎来到小说角色展示页 API！"}

app.include_router(
    characters.router, 
    prefix="/api/v1/characters", 
    tags=["Characters"]
)

app.include_router(
    utils.router,
    prefix="/api/v1/utils",
    tags=["Utils"]
)

app.include_router(
    ai.router,
    prefix="/api/v1/ai",
    tags=["AI"]
)