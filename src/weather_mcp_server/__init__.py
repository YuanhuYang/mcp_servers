"""
Weather MCP Server - 天气查询 MCP 服务器

这是一个基于 FastMCP 库构建的天气查询服务器，提供以下功能：
- get_alerts: 根据州名获取天气预警
- get_forecast: 根据经纬度获取天气预报

数据来源：美国国家气象局 (NWS) API
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

import httpx  # type: ignore
from fastmcp import FastMCP  # type: ignore
from pydantic import BaseModel, Field  # type: ignore

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 FastMCP 服务器
mcp = FastMCP("Weather MCP Server")

# NWS API 基础 URL
NWS_BASE_URL = "https://api.weather.gov"


class AlertsResponse(BaseModel):
    """天气预警响应模型"""
    type: str
    features: List[Dict[str, Any]]


class ForecastResponse(BaseModel):
    """天气预报响应模型"""
    properties: Dict[str, Any]


@mcp.tool()
async def get_alerts(
    state: str = Field(description="美国州名，例如：CA, NY, TX")
) -> Dict[str, Any]:
    """
    根据州名获取天气预警信息
    
    参数:
        state: 美国州名的两字母缩写（如 CA, NY, TX）
    
    返回:
        包含天气预警信息的字典
    """
    try:
        async with httpx.AsyncClient() as client:
            # 构建请求 URL
            url = f"{NWS_BASE_URL}/alerts/active"
            params = {"area": state.upper()}
            
            logger.info("正在获取 %s 州的天气预警信息...", state.upper())
            
            # 发送异步请求
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            
            data = response.json()
            
            # 提取关键信息
            alerts = []
            if "features" in data:
                for feature in data["features"]:
                    properties = feature.get("properties", {})
                    alert_info = {
                        "event": properties.get("event", "未知事件"),
                        "headline": properties.get("headline", "无标题"),
                        "description": properties.get("description", "无描述"),
                        "severity": properties.get("severity", "未知"),
                        "urgency": properties.get("urgency", "未知"),
                        "areas": properties.get("areaDesc", "未知区域"),
                        "effective": properties.get("effective", "未知时间"),
                        "expires": properties.get("expires", "未知时间")
                    }
                    alerts.append(alert_info)
            
            result = {
                "state": state.upper(),
                "total_alerts": len(alerts),
                "alerts": alerts
            }
            
            logger.info("成功获取 %d 条预警信息", len(alerts))
            return result
            
    except httpx.TimeoutException:
        error_msg = f"获取 {state.upper()} 州天气预警信息超时"
        logger.error(error_msg)
        return {"error": error_msg, "state": state.upper()}
    except httpx.HTTPStatusError as e:
        error_msg = f"获取 {state.upper()} 州天气预警信息失败: HTTP {e.response.status_code}"
        logger.error(error_msg)
        return {"error": error_msg, "state": state.upper()}
    except (ValueError, KeyError) as e:
        error_msg = f"解析天气预警数据失败: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "state": state.upper()}


@mcp.tool()
async def get_forecast(
    latitude: float = Field(description="纬度，例如：39.7456"),
    longitude: float = Field(description="经度，例如：-97.0892")
) -> Dict[str, Any]:
    """
    根据经纬度获取天气预报信息
    
    参数:
        latitude: 纬度
        longitude: 经度
    
    返回:
        包含天气预报信息的字典
    """
    try:
        async with httpx.AsyncClient() as client:
            # 首先获取网格点信息
            grid_url = f"{NWS_BASE_URL}/points/{latitude},{longitude}"
            
            logger.info("正在获取坐标 (%s, %s) 的天气预报...", latitude, longitude)
            
            # 获取网格点信息
            grid_response = await client.get(grid_url, timeout=10.0)
            grid_response.raise_for_status()
            grid_data = grid_response.json()
            
            # 提取预报 URL
            forecast_url = grid_data["properties"]["forecast"]
            
            # 获取天气预报
            forecast_response = await client.get(forecast_url, timeout=10.0)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            # 提取关键预报信息
            periods = forecast_data["properties"]["periods"]
            forecasts = []
            
            for period in periods[:7]:  # 只取前7个时段
                forecast_info = {
                    "name": period.get("name", "未知时段"),
                    "temperature": period.get("temperature", "未知"),
                    "temperature_unit": period.get("temperatureUnit", ""),
                    "wind_speed": period.get("windSpeed", "未知"),
                    "wind_direction": period.get("windDirection", "未知"),
                    "short_forecast": period.get("shortForecast", "无预报"),
                    "detailed_forecast": period.get("detailedForecast", "无详细预报")
                }
                forecasts.append(forecast_info)
            
            result = {
                "location": {
                    "latitude": latitude,
                    "longitude": longitude,
                    "city": grid_data["properties"].get("relativeLocation", {}).get("properties", {}).get("city", "未知城市"),
                    "state": grid_data["properties"].get("relativeLocation", {}).get("properties", {}).get("state", "未知州")
                },
                "forecast_periods": len(forecasts),
                "forecasts": forecasts,
                "updated": forecast_data["properties"].get("updated", "未知时间")
            }
            
            logger.info("成功获取 %d 个时段的天气预报", len(forecasts))
            return result
            
    except httpx.TimeoutException:
        error_msg = f"获取坐标 ({latitude}, {longitude}) 天气预报超时"
        logger.error(error_msg)
        return {"error": error_msg, "location": {"latitude": latitude, "longitude": longitude}}
    except httpx.HTTPStatusError as e:
        error_msg = f"获取坐标 ({latitude}, {longitude}) 天气预报失败: HTTP {e.response.status_code}"
        logger.error(error_msg)
        return {"error": error_msg, "location": {"latitude": latitude, "longitude": longitude}}
    except KeyError as e:
        error_msg = f"解析天气预报数据失败，缺少字段: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "location": {"latitude": latitude, "longitude": longitude}}
    except (ValueError, OSError) as e:
        error_msg = f"获取坐标 ({latitude}, {longitude}) 天气预报时发生错误: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "location": {"latitude": latitude, "longitude": longitude}}


def main():
    """启动 MCP 服务器"""
    logger.info("正在启动 Weather MCP Server...")
    mcp.run()


if __name__ == "__main__":
    main()
