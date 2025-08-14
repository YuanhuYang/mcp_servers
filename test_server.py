#!/usr/bin/env python3
"""
天气 MCP 服务器功能演示脚本
"""

import asyncio
import json

try:
    import httpx  # type: ignore
except ImportError:
    print("错误: 缺少 httpx 依赖包")
    print("请运行: pip install httpx")
    exit(1)


async def test_nws_api_directly():
    """直接测试 NWS API 连接"""
    print("=== 测试 NWS API 连接 ===")
    
    try:
        async with httpx.AsyncClient() as client:
            # 测试获取加利福尼亚州的天气预警
            print("1. 测试天气预警 API...")
            alerts_url = "https://api.weather.gov/alerts/active"
            params = {"area": "CA"}
            
            response = await client.get(alerts_url, params=params, timeout=10.0)
            response.raise_for_status()
            alerts_data = response.json()
            
            print(f"成功获取 {len(alerts_data.get('features', []))} 条预警信息")
            
            # 测试获取天气预报
            print("\n2. 测试天气预报 API...")
            latitude, longitude = 40.7128, -74.0060  # 纽约市
            
            grid_url = f"https://api.weather.gov/points/{latitude},{longitude}"
            grid_response = await client.get(grid_url, timeout=10.0)
            grid_response.raise_for_status()
            grid_data = grid_response.json()
            
            forecast_url = grid_data["properties"]["forecast"]
            forecast_response = await client.get(forecast_url, timeout=10.0)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            periods = forecast_data["properties"]["periods"]
            print(f"成功获取 {len(periods)} 个时段的天气预报")
            
            # 显示第一个预报
            if periods:
                first_period = periods[0]
                print("\n当前天气预报:")
                print(f"时段: {first_period.get('name', '未知')}")
                print(f"温度: {first_period.get('temperature', '未知')}°{first_period.get('temperatureUnit', '')}")
                print(f"简述: {first_period.get('shortForecast', '无')}")
        
        return True
        
    except httpx.RequestError as e:
        print(f"网络请求错误: {e}")
        return False
    except httpx.HTTPStatusError as e:
        print(f"HTTP 状态错误: {e.response.status_code}")
        return False
    except KeyError as e:
        print(f"API 响应格式错误，缺少字段: {e}")
        return False
    except (asyncio.TimeoutError, OSError) as e:
        print(f"连接超时或网络错误: {e}")
        return False
    except ValueError as e:
        print(f"数据解析错误: {e}")
        return False


async def main():
    """主函数"""
    print("Weather MCP Server - 功能演示\n")
    print("这个演示将测试:")
    print("1. NWS API 连接")
    print("2. 天气预警获取")
    print("3. 天气预报获取")
    print("-" * 50)
    
    api_ok = await test_nws_api_directly()
    
    if api_ok:
        print("\n" + "=" * 50)
        print("✅ API 测试通过！")
        print("\n📚 如何使用这个 MCP 服务器:")
        print("1. 启动服务器: python -m weather_mcp_server")
        print("2. 在支持 MCP 的客户端中配置此服务器")
        print("3. 使用工具:")
        print("   - get_alerts(state): 获取指定州的天气预警")
        print("   - get_forecast(latitude, longitude): 获取指定坐标的天气预报")
        
        print("\n🔧 MCP 配置示例 (.vscode/mcp.json):")
        mcp_config = {
            "servers": {
                "weather-mcp-server": {
                    "type": "stdio",
                    "command": "python",
                    "args": ["-m", "weather_mcp_server"]
                }
            }
        }
        print(json.dumps(mcp_config, indent=2))
    else:
        print("\n❌ API 测试失败，请检查网络连接")


if __name__ == "__main__":
    asyncio.run(main())
