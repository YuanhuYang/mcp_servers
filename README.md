# Weather MCP Server

一个基于 FastMCP 库构建的天气查询 MCP 服务器，提供实时天气预警和天气预报功能。

## 功能特性

- **get_alerts**: 根据美国州名获取天气预警信息
- **get_forecast**: 根据经纬度获取详细天气预报
- 基于美国国家气象局 (NWS) API
- 异步处理，高性能
- 标准 MCP 协议支持

## 技术栈

- **语言**: Python 3.8+
- **框架**: FastMCP
- **HTTP 客户端**: httpx (异步)
- **数据验证**: Pydantic
- **数据源**: 美国国家气象局 (NWS) API

## 安装

1. 克隆项目到本地
2. 安装依赖：

```bash
pip install -e .
```

## 使用方法

### 启动服务器

```bash
python -m weather_mcp_server
```

或者：

```bash
weather-mcp-server
```

### 工具说明

#### get_alerts(state)
根据州名获取天气预警信息

**参数:**
- `state` (str): 美国州名的两字母缩写（如 "CA", "NY", "TX"）

**返回:**
```json
{
  "state": "CA",
  "total_alerts": 2,
  "alerts": [
    {
      "event": "High Wind Warning",
      "headline": "High Wind Warning until 6 PM PST",
      "description": "Damaging winds expected...",
      "severity": "Moderate",
      "urgency": "Expected",
      "areas": "Los Angeles County",
      "effective": "2025-01-15T10:00:00-08:00",
      "expires": "2025-01-15T18:00:00-08:00"
    }
  ]
}
```

#### get_forecast(latitude, longitude)
根据经纬度获取天气预报

**参数:**
- `latitude` (float): 纬度
- `longitude` (float): 经度

**返回:**
```json
{
  "location": {
    "latitude": 39.7456,
    "longitude": -97.0892,
    "city": "Kansas City",
    "state": "KS"
  },
  "forecast_periods": 7,
  "forecasts": [
    {
      "name": "Today",
      "temperature": 45,
      "temperature_unit": "F",
      "wind_speed": "10 to 15 mph",
      "wind_direction": "NW",
      "short_forecast": "Partly Cloudy",
      "detailed_forecast": "Partly cloudy skies with..."
    }
  ],
  "updated": "2025-01-15T12:00:00+00:00"
}
```

## 开发

### 项目结构

```
weather-mcp-server/
├── src/
│   └── weather_mcp_server/
│       └── __init__.py          # 主要服务器代码
├── .github/
│   └── copilot-instructions.md  # Copilot 指令
├── .vscode/
│   ├── mcp.json                 # MCP 配置
│   └── tasks.json               # VS Code 任务
├── pyproject.toml               # 项目配置
└── README.md                    # 项目文档
```

### 在 VS Code 中调试

1. 打开项目
2. 使用 F5 启动调试
3. 服务器将通过 stdio 协议启动

## API 限制

- 仅支持美国境内的天气数据
- 依赖美国国家气象局 API 的可用性
- 建议实施适当的请求频率限制

## 许可证

MIT License

## 贡献

欢迎提交 Issues 和 Pull Requests！
