# --- Stage 1: Build Frontend Assets ---
# 使用 Vite 推荐的 Node.js LTS 版本 (20.x)
FROM node:20-alpine AS build-stage

WORKDIR /app

# 复制 frontend 目录下的 package.json 和 lock 文件
COPY ./frontend/package*.json ./
RUN npm config set registry https://registry.npmmirror.com
# 安装前端依赖
RUN npm install

# 复制整个 frontend 目录的源代码
COPY ./frontend/ ./

# 运行构建命令
RUN npm run build

# --- Stage 2: Production Nginx Server ---
FROM nginx:stable-alpine

# 从构建阶段复制打包好的静态文件到 Nginx 的网站根目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 复制自定义的 Nginx 配置文件
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]