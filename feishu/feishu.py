#!/usr/bin/env python3
"""
OpenClaw 飞书/ Lark 消息插件

功能：
- 接收飞书群消息
- 发送消息到飞书群/个人
- 消息处理和自动回复

安装：
    pip install requests cryptography
    # 配置 App ID 和 App Secret

配置（config.json）:
{
    "feishu": {
        "app_id": "cli_xxxxx",
        "app_secret": "xxxxx"
    }
}
"""
import json
import os
import time
import hashlib
import hmac
import base64
import requests
from cryptography.fernet import Fernet
from typing import Optional, Dict, List

# 飞书API配置
BASE_URL = "https://open.feishu.cn/open-apis"
APP_ID = ""
APP_SECRET = ""


class FeishuBot:
    """飞书Bot类"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.token_expires = 0
    
    def get_access_token(self) -> str:
        """获取access_token"""
        if self.access_token and time.time() < self.token_expires:
            return self.access_token
        
        url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        if data.get("code") == 0:
            self.access_token = data["tenant_access_token"]
            self.token_expires = time.time() + data.get("expire", 7200) - 300
            return self.access_token
        else:
            raise Exception(f"获取token失败: {data}")
    
    def send_message(self, receive_id_type: str, receive_id: str, msg_type: str = "text", content: str = "") -> Dict:
        """
        发送消息
        
        Args:
            receive_id_type: "open_id" / "user_id" / "union_id" / "chat_id"
            receive_id: 接收者ID
            msg_type: "text" / "rich_text" / "image" / "interactive"
            content: 消息内容
        
        Returns:
            Dict: API响应
        """
        url = f"{BASE_URL}/im/v1/messages"
        params = {
            "receive_id_type": receive_id_type
        }
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        # 构建消息内容
        if msg_type == "text":
            payload_content = {"text": content}
        elif msg_type == "rich_text":
            payload_content = {"text": content}
        else:
            payload_content = {"text": content}
        
        payload = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": json.dumps(payload_content)
        }
        
        response = requests.post(url, params=params, json=payload, headers=headers)
        return response.json()
    
    def send_text(self, receive_id_type: str, receive_id: str, text: str) -> Dict:
        """发送文本消息"""
        return self.send_message(receive_id_type, receive_id, "text", text)
    
    def send_to_chat(self, chat_id: str, text: str) -> Dict:
        """发送消息到群聊"""
        return self.send_text("chat_id", chat_id, text)
    
    def send_to_user(self, open_id: str, text: str) -> Dict:
        """发送消息给用户"""
        return self.send_text("open_id", open_id, text)
    
    def get_chat_info(self, chat_id: str) -> Dict:
        """获取群聊信息"""
        url = f"{BASE_URL}/im/v1/chats/{chat_id}"
        headers = {"Authorization": f"Bearer {self.get_access_token()}"}
        response = requests.get(url, headers=headers)
        return response.json()
    
    def get_chat_members(self, chat_id: str) -> List[Dict]:
        """获取群成员列表"""
        url = f"{BASE_URL}/im/v1/chats/{chat_id}/members"
        headers = {"Authorization": f"Bearer {self.get_access_token()}"}
        response = requests.get(url, headers=headers)
        data = response.json()
        if data.get("code") == 0:
            return data.get("data", {}).get("items", [])
        return []
    
    def create_webhook(self, name: str, url: str, chat_id: str = None) -> Dict:
        """创建Webhook"""
        url = f"{BASE_URL}/im/v1/webhooks"
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-Type": "application/json; charset=utf-8"
        }
        payload = {
            "name": name,
            "url": url,
            "chat_id": chat_id
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    
    def parse_message(self, event: Dict) -> Optional[Dict]:
        """
        解析消息事件
        
        Args:
            event: 飞书回调事件
        
        Returns:
            Dict: 解析后的消息
        """
        msg_type = event.get("message", {}).get("msg_type")
        content = event.get("message", {}).get("content", {})
        
        if msg_type == "text":
            text = content.get("text", "")
            return {
                "type": "text",
                "content": text,
                "message_id": event.get("message", {}).get("message_id"),
                "sender_id": event.get("sender", {}).get("sender_id", {}).get("open_id")
            }
        elif msg_type == "image":
            return {
                "type": "image",
                "image_key": content.get("image_key"),
                "message_id": event.get("message", {}).get("message_id")
            }
        
        return {"type": msg_type, "raw": content}


class MessageHandler:
    """消息处理器基类"""
    
    def __init__(self, bot: FeishuBot):
        self.bot = bot
    
    def handle(self, event: Dict) -> Optional[str]:
        """处理消息，返回回复内容"""
        raise NotImplementedError


class EchoHandler(MessageHandler):
    """回声处理器 - 自动回复相同内容"""
    
    def handle(self, event: Dict) -> Optional[str]:
        if event.get("type") == "text":
            return event.get("content", "")
        return None


class KeywordHandler(MessageHandler):
    """关键词自动回复"""
    
    def __init__(self, bot: FeishuBot, keywords: Dict[str, str]):
        super().__init__(bot)
        self.keywords = keywords
    
    def handle(self, event: Dict) -> Optional[str]:
        if event.get("type") == "text":
            content = event.get("content", "").lower()
            for keyword, response in self.keywords.items():
                if keyword.lower() in content:
                    return response
        return None


class AIHandler(MessageHandler):
    """AI对话处理器"""
    
    def __init__(self, bot: FeishuBot, ai_api_key: str = None):
        super().__init__(bot)
        self.ai_api_key = ai_api_key
    
    def handle(self, event: Dict) -> Optional[str]:
        """调用AI处理消息"""
        if event.get("type") == "text":
            content = event.get("content", "")
            
            # 这里可以接入任意AI API
            # 例如 OpenAI, Claude, 通义千问等
            # 示例使用简单的响应
            return f"收到消息: {content}"
        
        return None


# ============ OpenClaw Skill 封装 ============

SKILL_NAME = "feishu"
SKILL_VERSION = "1.0.0"
SKILL_DESCRIPTION = "飞书/ Lark 消息收发插件，支持群聊管理、自动回复"

SKILL_SCHEMA = {
    "name": SKILL_NAME,
    "version": SKILL_VERSION,
    "description": SKILL_DESCRIPTION,
    "commands": [
        {
            "name": "send_message",
            "description": "发送消息到飞书",
            "parameters": {
                "type": "object",
                "properties": {
                    "receive_id_type": {"type": "string", "enum": ["open_id", "user_id", "chat_id"]},
                    "receive_id": {"type": "string"},
                    "message": {"type": "string"}
                },
                "required": ["receive_id", "message"]
            }
        },
        {
            "name": "get_chat_info",
            "description": "获取群聊信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "chat_id": {"type": "string"}
                },
                "required": ["chat_id"]
            }
        }
    ]
}


def send_message(receive_id_type: str, receive_id: str, message: str, app_id: str = None, app_secret: str = None) -> str:
    """
    OpenClaw Skill: 发送飞书消息
    """
    global APP_ID, APP_SECRET
    
    if app_id: APP_ID = app_id
    if app_secret: APP_SECRET = app_secret
    
    if not APP_ID or not APP_SECRET:
        return "错误: 请配置 App ID 和 App Secret"
    
    try:
        bot = FeishuBot(APP_ID, APP_SECRET)
        result = bot.send_message(receive_id_type, receive_id, "text", message)
        
        if result.get("code") == 0:
            return f"✅ 消息发送成功! message_id: {result.get('data', {}).get('message_id')}"
        else:
            return f"❌ 发送失败: {result.get('msg')}"
    except Exception as e:
        return f"❌ 错误: {str(e)}"


def get_chat_info(chat_id: str, app_id: str = None, app_secret: str = None) -> str:
    """OpenClaw Skill: 获取群聊信息"""
    global APP_ID, APP_SECRET
    
    if app_id: APP_ID = app_id
    if app_secret: APP_SECRET = app_secret
    
    try:
        bot = FeishuBot(APP_ID, APP_SECRET)
        result = bot.get_chat_info(chat_id)
        
        if result.get("code") == 0:
            data = result.get("data", {})
            return f"""📋 群聊信息:
- 名称: {data.get('name', '未知')}
- ID: {data.get('chat_id', '未知')}
- 描述: {data.get('description', '无')}
- 头像: {data.get('avatar', '无')}"""
        else:
            return f"❌ 获取失败: {result.get('msg')}"
    except Exception as e:
        return f"❌ 错误: {str(e)}"


# CLI入口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("""
飞书消息插件 v1.0.0

用法:
    python feishu.py send <receive_id_type> <receive_id> <message>
    python feishu.py info <chat_id>
    python feishu.py chat_list

示例:
    python feishu.py send chat_id ou_xxxxx "你好"
    python feishu.py info ou_xxxxx
        """)
        sys.exit(1)
    
    # 简单CLI实现
    APP_ID = os.environ.get("FEISHU_APP_ID", "")
    APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
    
    cmd = sys.argv[1]
    
    if cmd == "send" and len(sys.argv) >= 5:
        _, _, receive_id_type, receive_id, message = sys.argv[:5]
        print(send_message(receive_id_type, receive_id, message, APP_ID, APP_SECRET))
    
    elif cmd == "info" and len(sys.argv) >= 3:
        _, chat_id = sys.argv[:3]
        print(get_chat_info(chat_id, APP_ID, APP_SECRET))
    
    else:
        print("参数错误")
