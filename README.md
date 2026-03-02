# OpenClaw 中文插件库

[![GitHub Repo](https://img.shields.io/badge/GitHub-Fangwenky%2Fopenclaw--plugins-blue)](https://github.com/Fangwenky/openclaw-plugins)
[![Python Version](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE)

> 国内首个聚焦中文场景的 OpenClaw 超级插件库

## 📋 项目简介

OpenClaw 中文插件库旨在为国内用户提供本土化的 OpenClaw 插件解决方案，降低使用门槛，填补中文生态空白。

## 🗂️ 插件列表

### 🎯 第一批插件

| 插件 | 类别 | 状态 | 说明 |
|------|------|------|------|
| [feishu](./feishu/) | 本土平台 | ✅ 完成 | 飞书/ Lark 消息收发 |
| github-cn | 开发者工具 | 🔄 开发中 | GitHub 中文助手 |
| kuaidi | 生活服务 | 📝 规划中 | 快递查询 |
| wechat | 本土平台 | 📝 规划中 | 微信消息 |

## 🚀 快速开始

### 安装插件

```bash
# 克隆整个插件库
git clone https://github.com/Fangwenky/openclaw-plugins.git

# 进入具体插件目录
cd feishu

# 安装依赖
pip install -r requirements.txt
```

### 使用插件

```python
# 例如使用飞书插件
from feishu import FeishuBot

bot = FeishuBot("your_app_id", "your_app_secret")
bot.send_to_chat("chat_id", "Hello!")
```

## 📚 文档

- [飞书插件文档](./feishu/README.md)
- [开发规范](./docs/DEVELOPMENT.md) (规划中)
- [贡献指南](./docs/CONTRIBUTING.md) (规划中)

## 🎯 规划插件

### 本土平台类
- [ ] 微信消息插件
- [ ] 钉钉消息插件
- [ ] 支付宝插件
- [ ] 小红书插件
- [ ] 抖音插件

### 开发者工具类
- [ ] GitHub 中文助手 (PR翻译/代码评审)
- [ ] Conda/uv 环境管理
- [ ] 本地代码调试

### 教育科研类
- [ ] 校园网认证
- [ ] 知网/万方文献
- [ ] 论文查重

### 生活服务类
- [ ] 快递查询 (菜鸟API)
- [ ] 社保公积金查询
- [ ] 外卖订单管理

## 🤝 贡献

欢迎贡献代码！请阅读 [贡献指南](./docs/CONTRIBUTING.md) 了解如何参与。

## 📄 许可证

Apache License 2.0 - 详见 [LICENSE](LICENSE)

---

Made with ❤️ for OpenClaw Chinese Community
