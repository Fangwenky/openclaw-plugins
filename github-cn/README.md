# OpenClaw GitHub 中文助手插件

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE)

> OpenClaw 中文插件库 - GitHub PR翻译、代码评审插件

## 📋 功能特性

| 功能 | 说明 |
|------|------|
| 📄 PR翻译 | 将PR标题、描述、变更文件翻译为中文 |
| 🔍 代码评审 | 自动分析PR变更，生成评审报告 |
| 📋 Issue翻译 | 将Issue翻译为中文 |
| 💬 自动回复 | 自动回复Issue和PR |
| 📊 统计信息 | PR/Issue统计数据 |

## 📦 安装

```bash
pip install requests
```

## ⚙️ 配置

### 方式一：环境变量

```bash
export GITHUB_TOKEN="ghp_xxxxx"
```

### 方式二：代码中配置

```python
from github_cn import GitHubAPI

github = GitHubAPI("ghp_xxxxx")
```

## 🚀 使用

### PR翻译

```python
from github_cn import translate_pr

# 翻译 PR
result = translate_pr("microsoft", "vscode", 12345)
print(result)
```

输出示例：

```
# 📄 PR 翻译

## 基本信息
- **标题**: Add new feature
- **描述**: This PR adds...
- **作者**: username
- **状态**: open
- **分支**: feature-branch → main

## 📝 变更文件 (5 个)
- src/main.py (+100 -10)
- src/utils.py (+50 -5)
...
```

### 代码评审

```python
from github_cn import review_pr

# 生成评审报告
result = review_pr("microsoft", "vscode", 12345)
print(result)
```

输出示例：

```
# 🔍 PR 代码评审报告

## 📊 变更概览
- **文件数**: 10
- **新增行**: +500
- **删除行**: -200
- **净变更**: +300

## 📁 变更文件

### 💻 代码文件

**src/main.py**
- 变更: +100 -10
- ⚠️ 文件较大(100行), 建议拆分成多个文件

## 💡 评审建议

1. **代码规范**: 检查是否符合项目代码规范
2. **测试**: 确认是否有对应的测试用例
...
```

### Issue翻译

```python
from github_cn import translate_issue

result = translate_issue("microsoft", "vscode", 123)
print(result)
```

## 🔧 CLI 使用

```bash
# PR翻译
python github_cn.py pr microsoft vscode 12345

# 代码评审
python github_cn.py review microsoft vscode 12345

# Issue翻译
python github_cn.py issue microsoft vscode 123
```

## 📁 项目结构

```
github-cn/
├── github_cn.py        # 主插件代码
├── README.md          # 使用文档
├── CHANGELOG.md       # 更新日志
├── requirements.txt   # Python依赖
└── examples/          # 使用示例
    ├── basic.py
    └── review.py
```

## 🔐 GitHub Token 获取

1. 打开 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并保存 Token

## ⚠️ 注意事项

- Token 需要有对应仓库的访问权限
- API 有调用频率限制 (5000次/小时)
- 建议使用私有 Token

## 📄 许可证

Apache License 2.0 - 详见 [LICENSE](LICENSE)

---

Made with ❤️ for OpenClaw Chinese Community
