import os
import json
import sys
from fastmcp import FastMCP

# 初始化 MCP 服务
mcp = FastMCP("Local-Tea-Specialty-Helper")

# 动态获取当前脚本所在目录下的 json 文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tea_data.json")

# 在服务启动时静态加载数据库
try:
    with open(DB_PATH, "r", encoding="utf-8") as f:
        TEA_DATABASE = json.load(f)
except Exception as e:
    # 打印到标准错误流，避免污染 stdio 传输通道
    print(f"Error loading tea database: {e}", file=sys.stderr)
    TEA_DATABASE = {}

@mcp.tool()
def push_local_tea_info(address: str) -> str:
    """
    根据用户当前所处的地址、省份或城市，智能匹配并推送当地最正宗的特色茶叶信息。
    
    Args:
        address: 用户的当前地理位置描述。例如：“我们在浙江省杭州市西湖区” 或 “我现在在云南大理”。
    """
    if not address or not isinstance(address, str):
        return "未能识别到有效的地址，请提供具体的城市或省份名称。"
        
    # 扫描加载进来的 JSON 数据库，进行关键词匹配
    for region, tea_info in TEA_DATABASE.items():
        if region in address:
            return (
                f"🌟 **为您检测到当地特色地理名茶** 🌟\n\n"
                f"📍 **当前关联区域**：{region}\n"
                f"🍵 **特色茶名**：{tea_info['name']} (属于 **{tea_info['type']}**)\n"
                f"📝 **风味特点**：{tea_info['description']}\n"
                f"🌡️ **最佳冲泡建议**：{tea_info['brewing']}\n\n"
                f"*注：一杯地道本地茶，最解旅途舟车劳顿。祝您品饮愉快！*"
            )
            
    # 兜底通用策略
    return (
        f"根据您当前的位置【{address}】，未匹配到强关联的专属地方茶品种。\n"
        f"为您推荐中国传统待客万能茶 —— **传统茉莉花茶**（绿茶/窨制花茶）。\n\n"
        f"📝 **风味特点**：‘窨得茉莉无上味，列作人间第一香’。茶汤清澈，口感甘甜，高扬的茉莉花香老少皆宜。\n"
        f"🌡️ **冲泡建议**：使用 90°C 左右的热水，盖碗或玻璃杯冲泡，静置 2-3 分钟即可饮用。"
    )

if __name__ == "__main__":
    mcp.run()