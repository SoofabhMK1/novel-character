# --- Stage 1: Build stage ---
FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# --- Stage 2: Final stage ---
FROM python:3.11-slim

# 设置一个非 root 用户，增加安全性
RUN useradd --create-home appuser
USER appuser
WORKDIR /home/appuser/app

# --- 新增的关键行 ---
# 将用户本地的 bin 目录添加到 PATH 环境变量中
ENV PATH="/home/appuser/.local/bin:${PATH}"

# 从构建阶段复制已安装的依赖
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

# 复制后端应用的所有代码
COPY ./app ./app
COPY ./alembic ./alembic
COPY alembic.ini .

# 暴露容器的 8001 端口
EXPOSE 8001

# 设置容器启动时要执行的命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]