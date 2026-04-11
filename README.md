# 教师与班级连接管理及文件传输系统

基于 Python Flask 框架开发的轻量级课堂辅助工具，用于教师与班级之间的连接管理和文件传输。

## 功能特点

### 教师功能
- 创建连接并生成20位唯一数字密钥
- 通过连接密钥上传多张图片和文字内容
- 自动保存图片到 static/cimg 目录
- 内容支持覆盖更新

### 班级功能
- 通过20位连接密钥验证身份
- 查看共享内容（图片左，文字右）
- 响应式布局，适配不同屏幕尺寸
- 自动刷新显示最新内容

### 安全特性
- 基于Cookie的连接保持机制
- SQL注入防护（参数化查询）
- XSS攻击防护（输入转义）
- 文件上传类型限制（仅允许图片）
- 安全的Cookie设置

## 技术栈

- **后端框架**: Flask 3.0.0
- **数据库**: SQLite 3
- **前端技术**: HTML5, CSS3, JavaScript (AJAX)

## 部署说明

### 方式一：Docker 部署（推荐）

#### 环境要求
- Docker
- Docker Compose

#### 快速启动

1. **构建并启动容器**
   ```bash
   docker-compose up -d
   ```

2. **访问应用**
   
   打开浏览器访问：http://127.0.0.1:5000

#### 常用命令

- 查看日志：`docker-compose logs -f`
- 停止服务：`docker-compose down`
- 重启服务：`docker-compose restart`

#### 数据持久化

数据会自动保存在以下位置：
- 数据库：`./app.db`
- 上传图片：`./static/cimg/`

---

### 方式二：传统 Python 部署

#### 环境要求

- Python 3.7 或更高版本

#### 安装步骤

1. **克隆或下载项目**
   ```bash
   cd e:\临时
   ```

2. **创建虚拟环境（推荐）**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **启动应用**
   ```bash
   python app.py
   ```

5. **访问应用**
   
   打开浏览器访问：http://127.0.0.1:5000

## 使用说明

### 教师端操作流程

1. 访问 http://127.0.0.1:5000/teacher
2. 点击"创建连接"，输入连接名称
3. 系统生成20位连接密钥，请妥善保存
4. 输入连接密钥并确认
5. 上传图片（可多选）和输入文字内容
6. 点击"保存分享内容"

### 班级端操作流程

1. 访问 http://127.0.0.1:5000/class
2. 输入教师提供的20位连接密钥
3. 点击"连接课堂"
4. 自动显示共享内容，每5秒自动刷新

## 项目结构

```
e:\临时/
├── app.py                 # Flask应用主文件
├── database.py            # 数据库操作模块
├── requirements.txt       # Python依赖
├── Dockerfile            # Docker镜像构建文件
├── docker-compose.yml    # Docker Compose配置
├── .dockerignore         # Docker忽略文件
├── README.md             # 部署说明文档
├── static/
│   └── cimg/             # 上传的图片存储目录
└── templates/
    ├── index.html        # 首页
    ├── teacher.html      # 教师管理页面
    └── class.html        # 班级课堂页面
```

## 数据库结构

### connection 表
- `key` (TEXT, PRIMARY KEY): 20位连接密钥
- `name` (TEXT): 连接名称

### share 表
- `id` (INTEGER, PRIMARY KEY): 自增ID
- `connection` (TEXT, FOREIGN KEY): 关联connection表的key
- `share` (TEXT): JSON格式的分享内容

## 注意事项

1. static/cimg 目录需要有读写权限
2. 首次运行会自动创建 app.db 数据库文件
3. 建议在生产环境中禁用 debug 模式
4. 生产环境请使用更安全的 SECRET_KEY 配置

## 开发环境

当前版本已在以下环境测试通过：
- Python 3.8+
- Windows 操作系统
- Chrome/Firefox 浏览器
