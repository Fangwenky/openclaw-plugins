# OpenClaw 飞书/ Lark 消息插件

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE)

> OpenClaw 中文插件库 - 飞书消息收发插件

## 📋 功能特性

| 功能 | 说明 |
|------|------|
| ✉️ 消息发送 | 发送文本、 rich_text、图片消息 |
| 👥 群管理 | 获取群信息、群成员列表 |
| 🔗 Webhook | 支持 Webhook 回调 |
| 🤖 自动回复 | 关键词回复、AI 对话 |
| 📱 消息接收 | 接收群消息、个人消息 |

## 📦 安装

```bash
# 克隆项目
git clone https://github.com/Fangwenky/openclaw-plugins.git
cd openclaw-plugins/feishu

# 安装依赖
pip install requests cryptography
```

## ⚙️ 配置

### 方式一：环境变量

```bash
export FEISHU_APP_ID="cli_xxxxx"
export FEISHU_APP_SECRET="xxxxx"
```

### 方式二：代码中配置

```python
from feishu import FeishuBot

bot = FeishuBot("cli_xxxxx", "xxxxx")
```

## 🚀 使用

### 基础使用

```python
from feishu import FeishuBot

# 初始化
bot = FeishuBot("cli_xxxxx", "your_app_secret")

# 发送消息到群
bot.send_to_chat("oc_xxxxx", "Hello!")

# 发送消息给用户
bot.send_to_user("ou_xxxxx", "你好!")
```

### OpenClaw Skill 使用

```python
from feishu import send_message, get_chat_info

# 发送消息
send_message("chat_id", "oc_xxxxx", "Hello!")

# 获取群信息
get_chat_info("oc_xxxxx")
```

### 命令行使用

```bash
# 发送消息
python feishu.py send chat_id oc_xxxxx "Hello"

# 获取群信息
python feishu.py info oc_xxxxx
```

## 📱 飞书应用配置

### 1. 创建应用

1. 打开 [飞书开放平台](https://open.feishu.cn/app/)
2. 创建自建应用
3. 获取 App ID 和 App Secret

### 2. 添加权限

需要添加以下权限：

| 权限名称 | 权限说明 |
|----------|-----------|
| im:message:send_as_bot | 发送消息 |
| im:message:receive | 接收消息 |
| im:message:send_to_bot_user | 给用户发送消息 |
| im:chat:admin | 管理群聊 |
| im:chat:member | 群成员管理 |

### 3. 启用 Bot

在应用后台 → 应用能力 → Bot → 启用 Bot 能力

### 4. 事件订阅（可选）

如果需要接收消息，需要配置事件回调：

1. 设置回调 URL（需要公网服务器）
2. 订阅事件：`im.message.message.created`

## 📁 项目结构

```
feishu/
├── feishu.py          # 主插件代码
├── README.md          # 使用文档
├── CHANGELOG.md       # 更新日志
├── requirements.txt   # Python依赖
└── examples/          # 使用示例
    ├── basic.py       # 基础示例
    ├── echo.py        # 自动回复示例
    └── ai_chat.py     # AI对话示例
```

## 🔧 开发示例

### 示例 1: 发送消息

```python
from feishu import FeishuBot

APP_ID = "cli_xxxxx"
APP_SECRET = "your_secret"

bot = FeishuBot(APP_ID, APP_SECRET)

# 发送文本消息
result = bot.send_to_chat("oc_群ID", "你好!")
print(result)
```

### 示例 2: 关键词自动回复

```python
from feishu import FeishuBot, KeywordHandler

bot = FeishuBot(APP_ID, APP_SECRET)

# 配置关键词回复
keywords = {
    "hello": "你好!有什么可以帮你的?",
    "help": "我可以帮你发送飞书消息,管理群聊等",
    "天气": "今天天气很好!"
}

handler = KeywordHandler(bot, keywords)

# 处理收到的消息
event = {"type": "text", "content": "hello"}
response = handler.handle(event)
if response:
    bot.send_to_user(event["sender_id"], response)
```

### 示例 3: AI 对话

```python
from feishu import FeishuBot, AIHandler

bot = FeishuBot(APP_ID, APP_SECRET)

# 接入 AI
handler = AIHandler(bot, ai_api_key="your-openai-key")

# 处理消息
event = {"type": "text", "content": "今天天气怎么样?"}
response = handler.handle(event)
if response:
    bot.send_to_user(event["sender_id"], response)
```

## 📝 API 参考

### FeishuBot 类

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_access_token()` | 获取访问令牌 | - |
| `send_message()` | 发送消息 | receive_id_type, receive_id, msg_type, content |
| `send_to_chat()` | 发送到群 | chat_id, text |
| `send_to_user()` | 发送给用户 | open_id, text |
| `get_chat_info()` | 获取群信息 | chat_id |
| `get_chat_members()` | 获取群成员 | chat_id |
| `parse_message()` | 解析消息事件 | event |

## 🐛 问题反馈

如有问题，请提交 [Issue](https://github.com/Fangwenky/openclaw-plugins/issues)

## 📄 许可证

Apache License 2.0 - 详见 [LICENSE](LICENSE)

---

Made with ❤️ for OpenClaw Chinese Community
