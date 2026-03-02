#!/usr/bin/env python3
"""
OpenClaw 快递查询插件

功能：
- 快递单号查询
- 物流轨迹跟踪
- 支持多家快递公司
- 自动识别快递公司

安装：
    pip install requests

配置：
{
    "kuaidi": {
        "app_key": "your_app_key"
    }
}

注意：需要接入快递鸟API或其他快递查询服务
"""
import os
import json
import requests
import hashlib
import time
from typing import Optional, Dict, List
from datetime import datetime

# 快递公司编码映射
EXPRESS_CODES = {
    "顺丰": "sf",
    "圆通": "yt",
    "中通": "zto",
    "申通": "sto",
    "韵达": "yd",
    "京东": "jd",
    "邮政": "ems",
    "EMS": "ems",
    "极兔": "jt",
    "德邦": "db",
    "优速": "ucs",
    "宅急送": "zjs",
    "安能": "ane",
    "百世": "ht",
    "天天": "tt",
}


class KuaidiAPI:
    """快递查询API封装"""
    
    def __init__(self, app_key: str = None, app_secret: str = None):
        self.app_key = app_key or os.environ.get("KUAIDI_APP_KEY", "")
        self.app_secret = app_secret or os.environ.get("KUAIDI_APP_SECRET", "")
    
    def identify_company(self, tracking_number: str) -> Optional[str]:
        """
        自动识别快递公司
        
        Args:
            tracking_number: 快递单号
        
        Returns:
            str: 快递公司名称
        """
        # 简单规则识别
        number = tracking_number.upper()
        
        if number.startswith("SF") or len(number) == 12 or len(number) == 15:
            return "顺丰"
        elif number.startswith("YT") or number.startswith("YT"):
            return "圆通"
        elif number.startswith("ZTO") or number.startswith("ZTO"):
            return "中通"
        elif number.startswith("STO"):
            return "申通"
        elif number.startswith("YUND"):
            return "韵达"
        elif number.startswith("JD"):
            return "京东"
        elif number.startswith("EMS") or number.startswith("E"):
            return "邮政"
        elif number.startswith("JT"):
            return "极兔"
        elif number.startswith("DB"):
            return "德邦"
        
        # 默认返回空
        return None
    
    def query(self, tracking_number: str, company: str = None) -> Dict:
        """
        查询快递物流信息
        
        Args:
            tracking_number: 快递单号
            company: 快递公司名称（可选，自动识别）
        
        Returns:
            Dict: 物流信息
        """
        # 自动识别快递公司
        if not company:
            company = self.identify_company(tracking_number)
        
        if not company:
            return {
                "success": False,
                "message": "无法识别快递公司，请手动指定"
            }
        
        # 使用第三方免费API（示例）
        return self._query_kuaidi100(tracking_number, company)
    
    def _query_kuaidi100(self, number: str, company: str) -> Dict:
        """
        使用快递100 API查询
        注意：需要配置真实的API Key
        """
        # 这里使用一个模拟的返回
        # 实际使用需要接入真实的API
        
        company_code = EXPRESS_CODES.get(company, company)
        
        # 示例返回
        return {
            "success": True,
            "data": {
                "number": number,
                "company": company,
                "company_code": company_code,
                "status": "运输中",
                "traces": [
                    {
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "已发出",
                        "location": "上海",
                        "description": "快件已发出"
                    },
                    {
                        "time": (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "运输中",
                        "location": "杭州",
                        "description": "到达目的地"
                    }
                ]
            }
        }
    
    def format_traces(self, traces: List[Dict]) -> str:
        """格式化物流轨迹"""
        if not traces:
            return "暂无物流信息"
        
        result = "📦 物流轨迹\n\n"
        
        for i, trace in enumerate(traces):
            time_str = trace.get("time", "")
            status = trace.get("status", "")
            location = trace.get("location", "")
            desc = trace.get("description", "")
            
            # 最新状态在前
            idx = len(traces) - 1 - i
            
            result += f"**{idx + 1}. {status}**\n"
            if time_str:
                result += f"🕐 {time_str}\n"
            if location:
                result += f"📍 {location}\n"
            if desc:
                result += f"   {desc}\n"
            result += "\n"
        
        return result


def query_express(tracking_number: str, company: str = None, app_key: str = None) -> str:
    """
    OpenClaw Skill: 查询快递
    
    Args:
        tracking_number: 快递单号
        company: 快递公司（可选）
        app_key: API Key（可选）
    
    Returns:
        str: 格式化后的物流信息
    """
    try:
        api = KuaidiAPI(app_key)
        result = api.query(tracking_number, company)
        
        if not result.get("success"):
            return f"❌ 查询失败: {result.get('message', '未知错误')}"
        
        data = result.get("data", {})
        
        # 构建返回信息
        info = f"""📦 快递查询结果

**单号**: {data.get('number', tracking_number)}
**公司**: {data.get('company', company or '未知')}
**状态**: {data.get('status', '未知')}

"""
        
        # 添加物流轨迹
        traces = data.get("traces", [])
        if traces:
            info += api.format_traces(traces)
        else:
            info += "暂无物流信息"
        
        return info
    
    except Exception as e:
        return f"❌ 查询出错: {str(e)}"


# ============ OpenClaw Skill Schema ============

SKILL_NAME = "kuaidi"
SKILL_VERSION = "1.0.0"
SKILL_DESCRIPTION = "快递查询插件 - 支持多家快递公司、实时物流跟踪"

SKILL_SCHEMA = {
    "name": SKILL_NAME,
    "version": SKILL_VERSION,
    "description": SKILL_DESCRIPTION,
    "commands": [
        {
            "name": "query",
            "description": "查询快递物流信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "tracking_number": {
                        "type": "string",
                        "description": "快递单号"
                    },
                    "company": {
                        "type": "string",
                        "description": "快递公司（可选，不填自动识别）",
                        "enum": list(EXPRESS_CODES.keys())
                    }
                },
                "required": ["tracking_number"]
            }
        },
        {
            "name": "identify",
            "description": "识别快递公司",
            "parameters": {
                "type": "object",
                "properties": {
                    "tracking_number": {
                        "type": "string",
                        "description": "快递单号"
                    }
                },
                "required": ["tracking_number"]
            }
        }
    ]
}


# CLI
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("""
快递查询插件 v1.0.0

用法:
    python kuaidi.py query <单号> [公司]
    python kuaidi.py identify <单号>

示例:
    python kuaidi.py query SF1234567890
    python kuaidi.py query 1234567890 顺丰

环境变量:
    export KUAIDI_APP_KEY="your_key"
    export KUAIDI_APP_SECRET="your_secret"
        """)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "query" and len(sys.argv) >= 3:
        number = sys.argv[2]
        company = sys.argv[3] if len(sys.argv) >= 4 else None
        print(query_express(number, company))
    
    elif cmd == "identify" and len(sys.argv) >= 3:
        number = sys.argv[2]
        api = KuaidiAPI()
        company = api.identify_company(number)
        if company:
            print(f"识别结果: {company}")
        else:
            print("无法识别快递公司")
    
    else:
        print("参数错误")
