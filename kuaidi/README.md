# OpenClaw 快递查询插件

> OpenClaw 中文插件库 - 快递物流查询插件

## 📋 功能特性

| 功能 | 说明 |
|------|------|
| 🔍 单号查询 | 查询快递物流信息 |
| 🏷️ 自动识别 | 自动识别快递公司 |
| 📊 物流轨迹 | 完整的物流轨迹跟踪 |
| 📱 多公司 | 支持多家快递公司 |

## 📦 支持的快递公司

- 顺丰速运
- 圆通速递
- 中通快递
- 申通快递
- 韵达速递
- 京东物流
- 中国邮政EMS
- 极兔速递
- 德邦物流
- 更多公司...

## 📦 安装

```bash
pip install requests
```

## 🚀 使用

### Python 使用

```python
from kuaidi import query_express

# 查询快递
result = query_express("SF1234567890")
print(result)
```

输出示例：

```
📦 快递查询结果

**单号**: SF1234567890
**公司**: 顺丰
**状态**: 运输中

📦 物流轨迹

**1. 已发出**
🕐 2026-03-02 10:30:00
📍 上海
   快件已发出

**2. 运输中**
🕐 2026-03-02 14:20:00
📍 杭州
   到达目的地
```

### 自动识别

```python
from kuaidi import KuaidiAPI

api = KuaidiAPI()
company = api.identify_company("SF1234567890")
print(company)  # 输出: 顺丰
```

### 命令行使用

```bash
# 查询快递
python kuaidi.py query SF1234567890

# 指定公司
python kuaidi.py query 1234567890 顺丰

# 识别公司
python kuaidi.py identify SF1234567890
```

## 📁 项目结构

```
kuaidi/
├── kuaidi.py        # 主插件代码
├── README.md        # 使用文档
├── CHANGELOG.md    # 更新日志
├── requirements.txt # 依赖
└── examples/        # 使用示例
```

## 🔐 配置

### 环境变量

```bash
export KUAIDI_APP_KEY="your_key"
export KUAIDI_APP_SECRET="your_secret"
```

## 📝 快递单号格式

| 公司 | 单号格式 |
|------|----------|
| 顺丰 | 12位或15位数字 |
| 圆通 | 以YT开头 |
| 中通 | 以ZTO开头 |
| 申通 | 以STO开头 |
| 韵达 | 以YUND开头 |
| 京东 | 以JD开头 |
| EMS | 以E开头 |

## ⚠️ 注意事项

- 免费API有调用限制
- 建议申请正式的快递API服务
- 部分快递可能暂时无法查询

## 📄 许可证

Apache License 2.0

---

Made with ❤️ for OpenClaw Chinese Community
