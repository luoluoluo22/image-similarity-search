# 图像相似度搜索系统

一个基于深度学习的图像相似度搜索系统，可以通过Web界面上传图片并搜索相似图像。

## 功能特点

- 基于ResNet50的图像特征提取
- Web界面支持图片上传和搜索
- 支持移动设备访问和拍照搜索
- 使用FAISS进行高效相似度搜索
- 支持Windows服务器部署

## 系统要求

- Windows Server 2012 R2 或更高版本
- Python 3.8+
- 足够的磁盘空间用于存储图像
- 建议有GPU支持（可选）

## 安装步骤

### 1. 环境准备

1. 下载并安装 Python：
   - 访问 [Python官网](https://www.python.org/downloads/windows/)
   - 下载 Python 3.x Windows 安装程序（64位）
   - 运行安装程序，**务必勾选 "Add Python to PATH"**
   - 验证安装：
     ```bash
     python --version
     ```

2. 下载 NSSM（用于Windows服务管理）：
   - 访问 [NSSM官网](https://nssm.cc/download)
   - 下载最新版本
   - 解压，将 win64 文件夹中的 nssm.exe 复制到 C:\Windows\System32

### 2. 离线安装（推荐）

1. 在有网络的环境中准备依赖：
   ```bash
   # 下载依赖的wheel文件
   pip download -r requirements.txt -d wheels/
   ```

2. 将项目文件和wheels文件夹复制到服务器

3. 在服务器上运行离线安装脚本：
   ```bash
   offline_install.bat
   ```

### 3. 在线安装

1. 创建部署目录：
   ```bash
   mkdir C:\apps\image_search
   cd C:\apps\image_search
   ```

2. 复制项目文件到部署目录

3. 创建虚拟环境并安装依赖：
   ```bash
   python -m venv venv
   call venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. 配置Windows服务：
   ```bash
   setup_service.bat
   ```

### 4. 配置防火墙

1. 打开 Windows 防火墙高级设置
2. 创建新的入站规则
3. 选择端口
4. 输入 5000
5. 允许连接
6. 规则命名为 "Image Search App"

## 使用方法

1. 访问Web界面：
   ```
   http://your_server_ip:5000
   ```

2. 上传图片或使用手机拍照
3. 系统会返回相似度最高的图片结果

## 文件结构

```
image_similarity_image_similarity_search/
├── web_app.py # Web应用主文件
├── image_search.py # 图像搜索引擎核心
├── requirements.txt # 依赖列表
├── logging_config.py # 日志配置
├── run_app.bat # 运行脚本
├── setup_service.bat # 服务安装脚本
├── offline_install.bat # 离线安装脚本
├── images/ # 图片目录
├── templates/ # 模板目录
│ └── index.html
└── wheels/ # 离线安装包目录
```
## 故障排查

1. 查看服务状态：
   ```bash
   nssm status ImageSearch
   ```

2. 查看日志：
   ```bash
   type C:\apps\image_search\logs\stdout.log
   type C:\apps\image_search\app.log
   ```

3. 直接运行应用测试：
   ```bash
   C:\apps\image_search\run_app.bat
   ```

## 更新部署

当需要更新代码时：

1. 停止服务：
   ```bash
   nssm stop ImageSearch
   ```

2. 更新文件

3. 重启服务：
   ```bash
   nssm start ImageSearch
   ```

## 注意事项

- 确保 images 目录中有足够的参考图片
- 定期检查 logs 目录下的日志文件
- 建议配置 SSL 证书以确保安全访问
- 可以配置 Nginx 作为反向代理

## 许可证

MIT License