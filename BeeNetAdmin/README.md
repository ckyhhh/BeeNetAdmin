# BeeAdmin（蜜蜂网管）

基于 CLI 的轻量网络管理系统，快速巡检、Ping/TCP 存活检验。

## 特性

- 🔍 **设备扫描** - 扫描 IP 段，自动发现设备并入库
- 🔧 **设备巡检** - 三段管道（采集→解析→渲染），TextFSM + Jinja2
- 💓 **存活检测** - Ping + TCP 检测，上下线通知
- 📋 **配置管理** - 运行/启动配置备份，左右对比差异
- ⚡ **即时登录** - SSH/Telnet Web 终端
- 🐝 **AI 助手** - DeepSeek API 分析终端输出
- 📤 **信息导出** - 可选字段导出设备信息

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python 3.12 + Django 5.2 + DRF + Celery |
| 数据库 | MySQL 8.0 + Redis 7 |
| 前端 | Vue3 + Element Plus + Pinia |
| 通信 | HTTP REST + WebSocket (Django Channels) |
| 部署 | Docker Compose |

## 快速开始

```bash
# 克隆项目
git clone https://github.com/dingtongbin/BeeNetAdmin.git
cd BeeNetAdmin

# 一键启动
docker-compose up -d

# 访问
# PC 前端: http://localhost:3000
# 手机前端: http://localhost:3001
# 后端 API: http://localhost:8000/api/v1/
```

首次访问自动跳转初始化页面，设置管理员密码和主加密密码。

## 项目结构

```
BeeNetAdmin/
├── backend/                ← Django 后端
│   ├── beeadmin/           ← 项目配置
│   ├── apps/               ← 业务应用
│   │   ├── accounts/       ← 用户认证
│   │   ├── devices/        ← 设备管理
│   │   ├── scanning/       ← 设备扫描
│   │   ├── inspection/     ← 巡检管理
│   │   ├── alive/          ← 存活检测
│   │   ├── terminal/       ← 终端连接
│   │   ├── notification/   ← 通知管理
│   │   ├── ai/             ← AI 助手
│   │   └── system/         ← 系统设置
│   └── engine/             ← 核心引擎
├── frontend-pc/            ← PC 前端
├── frontend-mobile/        ← 手机前端
├── templates/              ← TextFSM + Jinja2 模板
└── docker-compose.yml
```

## 核心架构

### 三段管道

```
采集 (collect) → 解析 (parse) → 渲染 (render)
  连接设备        TextFSM        Jinja2
  执行命令        解析输出        生成报告
  存入 Redis       存入 DB        导出文件
  立即断开        无需连接        无需连接
```

### 设计原则

- **不依赖 SNMP** - 纯 CLI 驱动，通过 SSH/Telnet 管理
- **连接最小化** - 连接只做连接的事，解析和渲染消费缓存
- **敏感信息加密** - AES-256-GCM 加盐加密存储
- **零侵入** - 不在目标设备安装任何软件

## License

[MIT](LICENSE)
