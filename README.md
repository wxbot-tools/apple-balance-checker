# Apple Balance Checker

一个用于管理和检查Apple礼品卡余额的Web应用程序。

## 📋 项目简介

Apple Balance Checker 是一个基于 Tornado 框架开发的 Web 应用，提供了友好的界面来管理 Apple 账户和代理配置，并支持自动检查礼品卡余额状态。

### ✨ 主要功能

- 🔐 **账户管理**
  - 添加/删除 Apple ID 账户
  - 支持多个国家/地区（美国、德国、英国、日本等31个国家）
  - 配置测活代码（礼品卡PIN）
  - 实时显示账户状态

- 🌐 **代理配置**
  - 支持代理服务商配置（目前支持922Proxy, 其他代理需要找作者适配即可）
  - 代理配置自动检测
  - 保存前强制验证代理可用性

- 📊 **状态监控**
  - 实时显示账户检查状态
  - 自动每10秒刷新状态
  - 区分账户可用/不可用状态

- 🎨 **现代化界面**
  - 基于 Bootstrap 4.5.2 的响应式设计
  - 美观的渐变色卡片界面
  - Font Awesome 图标增强视觉效果

## 🔧 环境要求

### 系统要求
- 操作系统：Windows / macOS / Linux
- 浏览器：Chrome、Firefox、Safari、Edge（最新版本）

### Python版本
- **Python 3.10.12**（严格要求，其他版本可能导致兼容性问题）

### 依赖库
详见 `requirements.txt`

## 🚀 快速开始（Windows）

### 准备工作

#### 1. 安装Python 3.10.12

**必须安装此版本！** 其他版本可能导致兼容性问题。

1. 访问 Python 官方下载页面：
   ```
   https://www.python.org/downloads/release/python-31012/
   ```

2. 下载 Windows 安装包：
   - 64位系统：`Windows x86-64 executable installer`
   - 32位系统：`Windows x86 executable installer`

3. 运行安装程序：
   - ✅ **重要**：勾选 "Add Python 3.10 to PATH"
   - 点击 "Install Now"

4. 验证安装：
   ```bash
   python --version
   # 应该显示: Python 3.10.12
   ```

#### 2. 准备Chrome浏览器

本程序需要Chrome浏览器支持。脚本会自动检测：

**方式1：已安装Chrome**
- 如果系统已安装Chrome，脚本会自动检测并继续

**方式2：使用ChromeSetup.exe**
- 将 `ChromeSetup.exe` 放在项目根目录
- 脚本会在检测到Chrome未安装时自动运行安装程序

**方式3：手动安装**
- 访问：https://www.google.com/chrome/
- 下载并安装Chrome浏览器

#### 3. 下载项目

```bash
git clone <repository-url>
cd apple-balance-checker
```

或直接下载ZIP压缩包并解压。

### 🎯 一键启动

项目已配置好一键启动脚本，自动完成所有检查和配置：

#### 双击运行 `start.bat`

脚本会自动执行：
1. ✅ 检查Python版本（要求3.10.12）
2. ✅ 检查Chrome浏览器（未安装则自动安装）
3. ✅ 安装Python依赖
4. ✅ 启动Web服务器

#### 或在命令行运行

```bash
start.bat
```

### 首次运行

首次运行时，脚本会：
- 安装所需依赖包到系统Python（约需2-5分钟）
- 下载Playwright浏览器驱动（约需50-100MB）

后续运行将直接启动，无需等待。

**注意**：依赖包将安装到系统Python 3.10.12环境中。

### 访问应用

服务器启动后，浏览器会自动打开管理页面：
```
http://localhost/view/index
```

如未自动打开，请手动访问上述地址。

## 📁 项目结构

```
apple-balance-checker/
├── controller/              # 控制器层
│   ├── __init__.py         # 基础控制器
│   ├── balance.py          # 余额检查控制器
│   ├── config.py           # 配置管理控制器
│   └── view.py             # 视图控制器
├── model/                   # 数据模型层
│   ├── __init__.py         # 基础模型
│   └── balance_checker_account.py  # 账户模型
├── service/                 # 业务逻辑层
│   ├── __init__.py
│   ├── balance_checker.py  # 余额检查服务
│   ├── balance_checker_manager.py  # 检查器管理服务
│   └── config_service.py   # 配置服务
├── views/                   # 前端视图
│   └── index.html          # 主页面
├── balance_check_accounts.json  # 账户配置文件
├── proxy_config.json        # 代理配置文件
├── config.py                # 全局配置
├── web_app.py              # Web应用入口
├── requirements.txt         # Python依赖
└── README.md               # 项目说明
```

## ⚙️ 配置说明

### 代理配置 (proxy_config.json)

```json
{
  "provider": "922proxy",
  "server": "127.0.0.1:7890",
  "username": "your_username",
  "password": "your_password"
}
```

### 账户配置 (balance_check_accounts.json)

```json
[
  {
    "apple_id": "your_email@example.com",
    "password": "your_password",
    "country": "us",
    "check_pin": "X123456789ABCDEF"
  }
]
```

## 🎯 使用指南

### 1. 配置代理

1. 在"代理配置"模块中选择代理服务商（目前支持922Proxy）
2. 输入代理服务器地址
3. 输入用户名和密码
4. 点击"保存"按钮
   - 系统会自动检测代理可用性
   - 只有检测通过才会保存配置

### 2. 管理账户

1. 在"Balance Checker 账户管理"模块点击"新增账户"
2. 填写以下信息：
   - **Apple ID**：你的Apple账户邮箱
   - **密码**：Apple账户密码
   - **国家/地区**：从下拉框选择
   - **测活代码**：用于检查状态的礼品卡PIN码
3. 点击"添加账户"

### 3. 查看状态

- 账户列表会自动显示每个账户的当前状态
- 状态类型：
  - 🟢 **正常**：账户可用
  - 🟡 **不可用**：账户暂时不可用
- 状态每10秒自动刷新

### 4. 删除账户

在账户列表中点击对应账户的"删除"按钮，确认后即可删除。

## 🌍 支持的国家/地区

| 代码 | 国家/地区 | 代码 | 国家/地区 | 代码 | 国家/地区 |
|------|----------|------|----------|------|----------|
| us | 美国 | de | 德国 | gb | 英国 |
| ca | 加拿大 | au | 澳大利亚 | hk | 香港 |
| tw | 台湾 | jp | 日本 | kr | 韩国 |
| sg | 新加坡 | nz | 新西兰 | fr | 法国 |
| it | 意大利 | es | 西班牙 | nl | 荷兰 |
| be | 比利时 | ch | 瑞士 | at | 奥地利 |
| se | 瑞典 | no | 挪威 | dk | 丹麦 |
| ie | 爱尔兰 | pl | 波兰 | cz | 捷克 |
| hu | 匈牙利 | ro | 罗马尼亚 | bg | 保加利亚 |
| gr | 希腊 | pt | 葡萄牙 | sk | 斯洛伐克 |
| si | 斯洛文尼亚 |

## 🔒 安全建议

- ⚠️ **不要将配置文件提交到公共仓库**
- 建议在 `.gitignore` 中添加：
  ```
  balance_check_accounts.json
  proxy_config.json
  __pycache__/
  *.pyc
  venv/
  ```
- 定期更改密码
- 使用强密码
- 在安全的网络环境中使用

## 📥 获取ChromeSetup.exe

如果需要使用脚本自动安装Chrome功能，请将Chrome安装程序重命名为 `ChromeSetup.exe` 并放在项目根目录。

下载地址：https://www.google.com/chrome/

**注意**：`ChromeSetup.exe` 文件较大（约100MB），已添加到 `.gitignore`，不会提交到代码仓库。

## 🐛 常见问题

### 1. Python版本不匹配

**问题**：运行 `start.bat` 时提示版本错误并退出

**解决方法**：
- 必须安装 Python 3.10.12
- 卸载其他Python版本或确保3.10.12在PATH中优先
- 下载地址：https://www.python.org/downloads/release/python-31012/

### 2. Chrome浏览器检测失败

**问题**：脚本提示未检测到Chrome浏览器

**解决方法**：
- **方法1**：将 `ChromeSetup.exe` 放在项目根目录，脚本会自动安装
- **方法2**：手动安装Chrome：https://www.google.com/chrome/
- 安装后重新运行 `start.bat`

### 3. Playwright浏览器驱动安装失败

**问题**：提示找不到浏览器或浏览器启动失败

**解决方法**：
```bash
# 手动安装
playwright install chromium
```

### 4. 端口被占用

**问题**：启动时提示端口已被使用

**解决方法**：
- 修改 `config.py` 中的 `port` 值（默认80）
- 或者关闭占用80端口的其他程序

### 5. 代理检测失败

**问题**：保存代理配置时检测失败

**解决方法**：
- 检查代理服务器地址格式（应为 `host:port`，例如：`127.0.0.1:7890`）
- 确认代理服务商选择正确（目前仅支持922Proxy, 其他需要找作者适配）
- 验证用户名和密码是否正确
- 确保代理服务正在运行
- 测试代理网络连通性

### 6. 无法访问Web界面

**问题**：浏览器无法打开管理页面

**解决方法**：
- 确认服务已成功启动（查看命令行窗口输出）
- 检查Windows防火墙设置，允许Python通过防火墙
- 尝试使用 `http://127.0.0.1/view/index`
- 检查是否有杀毒软件拦截

### 7. 依赖安装失败

**问题**：pip install 时出错或速度慢

**解决方法**：
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像源（推荐）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用阿里云镜像
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

## 🔄 更新日志

### v1.0.0 (当前版本)
- ✅ 基础账户管理功能
- ✅ 代理配置与检测
- ✅ 实时状态监控
- ✅ 响应式Web界面
- ✅ 支持31个国家/地区

## 🛠️ 开发说明

### 技术栈

- **后端**：
  - Python 3.10.12
  - Tornado 6.x (异步Web框架)
  - Playwright (浏览器自动化)
  - httpx (HTTP客户端)
  - loguru (日志记录)

- **前端**：
  - HTML5 + CSS3 + JavaScript
  - Bootstrap 4.5.2
  - Font Awesome 5.15.4
  - jQuery 3.5.1

### API接口

#### 配置管理
- `GET /config/proxy` - 获取代理配置
- `POST /config/proxy` - 保存代理配置
- `POST /config/check_proxy` - 检测代理
- `GET /config/balance_check_account` - 获取账户列表
- `POST /config/balance_check_account` - 添加账户
- `DELETE /config/balance_check_account?apple_id=xxx` - 删除账户

#### 余额检查
- `GET /balance/checker_status` - 获取检查器状态
- `POST /balance/check` - 执行余额检查

#### 视图
- `GET /view/index` - 访问主页面

### 本地开发

```bash
# 开启调试模式
# 编辑 web_app.py，设置 debug=True
configs = {
    'debug': True,  # 开启后会自动重载代码
    ...
}
```

## 📝 许可证

本项目仅供学习和研究使用。请遵守相关法律法规，不要用于非法用途。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 发送邮件至：[your-email@example.com]

---

**⚠️ 免责声明**

本工具仅供学习和研究使用。使用本工具产生的任何后果由使用者自行承担。开发者不对因使用本工具而导致的任何直接或间接损失承担责任。

---

**Made with ❤️ by [Your Name]**
