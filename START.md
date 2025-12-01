# Django博客项目启动指南

## 快速开始

### 1. 安装依赖

在Windows上，您可能需要先安装Visual Studio C++构建工具，然后运行：

```bash
pip install -r requirements.txt
```

如果遇到mysqlclient安装问题，请尝试：

```bash
pip install mysqlclient
```

或者在Ubuntu/Debian系统上：

```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

### 2. 初始化数据库

```bash
python init_db.py
```

这将执行以下操作：
- 创建SQLite数据库文件 (db.sqlite3)
- 创建所有数据表
- 创建超级用户 (admin/admin123)

### 3. 启动服务器

```bash
python run_server.py
```

服务器将在以下地址运行：
- API服务: http://localhost:8002
- 管理后台: http://localhost:8002/admin

### 4. 启动前端

前端代码在原项目目录中，需要单独启动：

```bash
cd ../system_study/frontend
npm run serve
```

前端将在 http://localhost:8085 运行

## 项目结构说明

```
django_blog/
├── django_blog/      # Django项目配置
├── accounts/         # 用户认证模块
├── blog/             # 博客功能模块
├── media/            # 上传文件目录
├── requirements.txt  # Python依赖
├── manage.py         # Django管理命令
├── init_db.py        # 数据库初始化脚本
└── run_server.py     # 服务器启动脚本
```

## 管理后台

访问地址: http://localhost:8002/admin
默认超级用户:
- 用户名: admin
- 密码: admin123

## API接口

所有API接口都在 `/api/v1/` 前缀下：

- 认证: `/api/v1/auth/`
- 文章: `/api/v1/articles/`
- 分类: `/api/v1/categories/`
- 搜索: `/api/v1/articles/search/`
- 上传: `/api/v1/upload/`

## 常见问题

### 1. 数据库迁移问题

如果遇到数据库迁移问题，可以删除 `db.sqlite3` 文件和 `accounts/migrations/`、`blog/migrations/` 目录下的迁移文件，然后重新运行 `init_db.py`。

### 2. 依赖安装问题

如果安装依赖时遇到问题，请确保使用的是Python 3.8+版本，并且已安装了必要的编译工具。

### 3. 前端代理配置

前端默认将API请求代理到 `http://localhost:8002`，如需修改，请更新 `system_study/frontend/vue.config.js` 中的代理配置。