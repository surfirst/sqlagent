# LangChain SQL Agent 自然语言查询演示

这个项目演示如何使用 LangChain 的 SQLAgent 实现通过自然语言来查询数据库。

## 环境准备

### 安装依赖
使用以下命令安装所有必要的依赖包：
```bash
pip install -r requirements.txt
```

### 准备数据库
1. 安装 SQLite  
我们的例子里使用的是 SQLite 数据库，在 Linux 上可以使用 `sudo apt install sqlite3` 来安装。

2. 创建数据库  
使用以下命令创建数据库：
```bash
sqlite3 Chinook.db
```

3. 导入数据  
使用以下命令导入示例数据：
```bash
sqlite3 Chinook.db < Chinook_Sqlite.sql
```

## 环境变量配置
创建 `.env` 文件并根据您使用的模型配置相应的环境变量：

### Azure OpenAI（默认）
```env
MODEL_TYPE=azure
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### OpenAI 兼容模型
```env
MODEL_TYPE=openai
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=https://api.example.com/v1  # 兼容模型的API地址
MODEL_NAME=model_name  # 如：qwen-max 等
```

## 支持的模型
- Azure OpenAI (默认)
- OpenAI
- 通义千问
- 其他 OpenAI 兼容接口的模型

## 项目结构
```
.
├── README.md
├── .env
├── main.py
├── Chinook.db
└── Chinook_Sqlite.sql
```

## 使用方法
1. 确保已完成环境准备和配置
2. 运行应用：
```bash
python main.py
```
3. 输入您的自然语言查询，例如：
   - "显示所有客户的名字和邮箱"
   - "查询销售额最高的5个员工"

## 数据库架构
Chinook 数据库包含以下表：
- Customer（客户信息）
- Employee（员工信息）
- Invoice（订单信息）
- Track（音轨信息）
- Album（专辑信息）
- Artist（艺术家信息）

## 注意事项
- 请确保您的 API 密钥有足够的额度
- 建议在测试阶段设置合理的 token 限制以控制成本
- 不同模型的性能和成本可能有所不同，请根据实际需求选择
