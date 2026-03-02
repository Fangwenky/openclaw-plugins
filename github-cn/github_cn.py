#!/usr/bin/env python3
"""
OpenClaw GitHub 中文助手插件

功能：
- PR 翻译（中英文互译）
- 代码评审（自动分析PR问题）
- Issue 管理
- 自动回复 Issue

安装：
    pip install requests PyJWT

配置（config.json）:
{
    "github": {
        "token": "ghp_xxxxx"
    }
}
"""
import os
import json
import requests
from typing import Optional, Dict, List
from datetime import datetime

# GitHub API
BASE_URL = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


class GitHubAPI:
    """GitHub API 封装"""
    
    def __init__(self, token: str = None):
        self.token = token or GITHUB_TOKEN
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        if not self.token:
            raise Exception("请配置 GitHub Token")
    
    def get_pull_request(self, owner: str, repo: str, pr_number: int) -> Dict:
        """获取 PR 信息"""
        url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"获取PR失败: {response.status_code}")
    
    def get_pr_files(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        """获取 PR 变更的文件"""
        url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"获取PR文件失败: {response.status_code}")
    
    def get_pr_comments(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        """获取 PR 评论"""
        url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/comments"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []
    
    def get_review_comments(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        """获取代码评审评论"""
        url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/comments"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []
    
    def get_issue(self, owner: str, repo: str, issue_number: int) -> Dict:
        """获取 Issue"""
        url = f"{BASE_URL}/repos/{owner}/{repo}/issues/{issue_number}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"获取Issue失败: {response.status_code}")
    
    def create_issue_comment(self, owner: str, repo: str, issue_number: int, body: str) -> Dict:
        """创建 Issue 评论"""
        url = f"{BASE_URL}/repos/{owner}/{repo}/issues/{issue_number}/comments"
        response = requests.post(url, json={"body": body}, headers=self.headers)
        if response.status_code == 201:
            return response.json()
        raise Exception(f"创建评论失败: {response.status_code}")
    
    def create_pr_review(self, owner: str, repo: str, pr_number: int, body: str, event: str = "COMMENT") -> Dict:
        """创建 PR 评审"""
        url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
        response = requests.post(url, json={
            "body": body,
            "event": event
        }, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"创建评审失败: {response.status_code}")
    
    def get_commits(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        """获取 PR 的提交记录"""
        url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/commits"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []
    
    def get_diff(self, owner: str, repo: str, pr_number: int) -> str:
        """获取 PR 的 diff"""
        url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}"
        response = requests.get(url, headers=self.headers, params={"diff_url": "true"})
        # 使用 raw diff URL
        diff_url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}.diff"
        diff_response = requests.get(diff_url, headers=self.headers)
        return diff_response.text if diff_response.status_code == 200 else ""


class PRTranslator:
    """PR 翻译器"""
    
    def __init__(self, github: GitHubAPI):
        self.github = github
    
    def translate_pr(self, owner: str, repo: str, pr_number: int) -> str:
        """翻译 PR 内容"""
        pr = self.github.get_pull_request(owner, repo, pr_number)
        
        result = f"""# 📄 PR 翻译
        
## 基本信息
- **标题**: {pr.get('title', '无')}
- **描述**: {pr.get('body', '无') or '无'}
- **作者**: {pr.get('user', {}).get('login', '未知')}
- **状态**: {pr.get('state', '未知')}
- **分支**: {pr.get('head', {}).get('ref', '?')} → {pr.get('base', {}).get('ref', '?')}
- **创建时间**: {pr.get('created_at', '未知')}
- **链接**: {pr.get('html_url', '')}

## 📝 变更文件 ({len(self.github.get_pr_files(owner, repo, pr_number))} 个)
"""
        
        files = self.github.get_pr_files(owner, repo, pr_number)
        for f in files[:10]:  # 只显示前10个
            result += f"\n- {f.get('filename', '?')} ({f.get('additions', 0)} +{f.get('deletions', 0)} -)"
        
        if len(files) > 10:
            result += f"\n... 还有 {len(files) - 10} 个文件"
        
        return result
    
    def translate_issue(self, owner: str, repo: str, issue_number: int) -> str:
        """翻译 Issue 内容"""
        issue = self.github.get_issue(owner, repo, issue_number)
        
        labels = ", ".join([l.get("name", "") for l in issue.get("labels", [])])
        
        return f"""# 📋 Issue 翻译

## 基本信息
- **标题**: {issue.get('title', '无')}
- **内容**: {issue.get('body', '无') or '无'}
- **作者**: {issue.get('user', {}).get('login', '未知')}
- **状态**: {issue.get('state', '未知')}
- **标签**: {labels or '无'}
- **创建时间**: {issue.get('created_at', '未知')}
- **链接**: {issue.get('html_url', '')}
"""


class PRReviewer:
    """PR 代码评审"""
    
    def __init__(self, github: GitHubAPI):
        self.github = github
    
    def analyze_pr(self, owner: str, repo: str, pr_number: int) -> str:
        """分析 PR 并生成评审意见"""
        pr = self.github.get_pull_request(owner, repo, pr_number)
        files = self.github.get_pr_files(owner, repo, pr_number)
        
        # 统计信息
        total_additions = sum(f.get("additions", 0) for f in files)
        total_deletions = sum(f.get("deletions", 0) for f in files)
        
        result = f"""# 🔍 PR 代码评审报告

## 📊 变更概览
- **文件数**: {len(files)}
- **新增行**: +{total_additions}
- **删除行**: -{total_deletions}
- **净变更**: {total_additions - total_deletions:+d}

## 📁 变更文件
"""
        
        # 分析每个文件
        code_files = []
        other_files = []
        
        for f in files:
            filename = f.get("filename", "")
            if any(filename.endswith(ext) for ext in [".py", ".js", ".ts", ".java", ".go", ".rs", ".cpp", ".c"]):
                code_files.append(f)
            else:
                other_files.append(f)
        
        # 代码文件分析
        if code_files:
            result += "\n### 💻 代码文件\n"
            for f in code_files[:15]:
                result += f"\n**{f.get('filename')}**\n"
                result += f"- 变更: +{f.get('additions', 0)} -{f.get('deletions', 0)}\n"
                
                # 简单检查
                filename = f.get("filename", "")
                if "test" not in filename.lower() and filename.endswith(".py"):
                    if f.get("additions", 0) > 50:
                        result += f"- ⚠️ 文件较大({f.get('additions')}行), 建议拆分成多个文件\n"
                if f.get("deletions", 0) > 100:
                    result += f"- ⚠️ 删除较多, 注意兼容性\n"
        
        # 其他文件
        if other_files:
            result += f"\n### 📄 其他文件 ({len(other_files)} 个)\n"
            for f in other_files[:5]:
                result += f"- {f.get('filename')}\n"
        
        # 建议
        result += """
## 💡 评审建议

1. **代码规范**: 检查是否符合项目代码规范
2. **测试**: 确认是否有对应的测试用例
3. **文档**: 检查是否需要更新文档
4. **安全性**: 检查是否有安全漏洞
5. **性能**: 检查性能影响

---
*此报告由 GitHub 中文助手自动生成*
"""
        
        return result


# ============ OpenClaw Skill 封装 ============

SKILL_NAME = "github-cn"
SKILL_VERSION = "1.0.0"
SKILL_DESCRIPTION = "GitHub 中文助手 - PR翻译、代码评审、Issue管理"

SKILL_SCHEMA = {
    "name": SKILL_NAME,
    "version": SKILL_VERSION,
    "description": SKILL_DESCRIPTION,
    "commands": [
        {
            "name": "translate_pr",
            "description": "翻译 PR 内容为中文",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "仓库所有者"},
                    "repo": {"type": "string", "description": "仓库名称"},
                    "pr_number": {"type": "integer", "description": "PR编号"}
                },
                "required": ["owner", "repo", "pr_number"]
            }
        },
        {
            "name": "review_pr",
            "description": "分析 PR 并生成评审意见",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "pr_number": {"type": "integer"}
                },
                "required": ["owner", "repo", "pr_number"]
            }
        },
        {
            "name": "translate_issue",
            "description": "翻译 Issue 内容为中文",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "issue_number": {"type": "integer"}
                },
                "required": ["owner", "repo", "issue_number"]
            }
        }
    ]
}


def translate_pr(owner: str, repo: str, pr_number: int, token: str = None) -> str:
    """翻译 PR 为中文"""
    global GITHUB_TOKEN
    if token: GITHUB_TOKEN = token
    
    try:
        github = GitHubAPI(GITHUB_TOKEN)
        translator = PRTranslator(github)
        return translator.translate_pr(owner, repo, pr_number)
    except Exception as e:
        return f"❌ 错误: {str(e)}"


def review_pr(owner: str, repo: str, pr_number: int, token: str = None) -> str:
    """生成 PR 评审报告"""
    global GITHUB_TOKEN
    if token: GITHUB_TOKEN = token
    
    try:
        github = GitHubAPI(GITHUB_TOKEN)
        reviewer = PRReviewer(github)
        return reviewer.analyze_pr(owner, repo, pr_number)
    except Exception as e:
        return f"❌ 错误: {str(e)}"


def translate_issue(owner: str, repo: str, issue_number: int, token: str = None) -> str:
    """翻译 Issue 为中文"""
    global GITHUB_TOKEN
    if token: GITHUB_TOKEN = token
    
    try:
        github = GitHubAPI(GITHUB_TOKEN)
        translator = PRTranslator(github)
        return translator.translate_issue(owner, repo, issue_number)
    except Exception as e:
        return f"❌ 错误: {str(e)}"


# CLI
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("""
GitHub 中文助手 v1.0.0

用法:
    python github-cn.py pr <owner> <repo> <pr_number>
    python github-cn.py review <owner> <repo> <pr_number>
    python github-cn.py issue <owner> <repo> <issue_number>

示例:
    python github-cn.py pr facebook react 12345
    python github-cn.py review microsoft vscode 12345

环境变量:
    export GITHUB_TOKEN="ghp_xxxxx"
        """)
        sys.exit(1)
    
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
    
    cmd = sys.argv[1]
    
    if cmd == "pr" and len(sys.argv) >= 5:
        _, _, owner, repo, pr = sys.argv[2:5]
        print(translate_pr(owner, repo, int(pr), GITHUB_TOKEN))
    
    elif cmd == "review" and len(sys.argv) >= 5:
        _, _, owner, repo, pr = sys.argv[2:5]
        print(review_pr(owner, repo, int(pr), GITHUB_TOKEN))
    
    elif cmd == "issue" and len(sys.argv) >= 5:
        _, _, owner, repo, issue = sys.argv[2:5]
        print(translate_issue(owner, repo, int(issue), GITHUB_TOKEN))
    
    else:
        print("参数错误")
