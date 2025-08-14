<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Weather MCP Server - Copilot Instructions

这是一个基于 FastMCP 库的天气查询 MCP 服务器项目。

## 项目上下文

- **项目类型**: Model Context Protocol (MCP) 服务器
- **主要功能**: 提供天气预警和天气预报查询服务
- **数据源**: 美国国家气象局 (NWS) API
- **技术栈**: Python, FastMCP, httpx, Pydantic

## 开发指南

### 核心组件
- 使用 `@mcp.tool()` 装饰器注册工具函数
- 所有 API 调用都应该是异步的 (`async/await`)
- 使用 `httpx.AsyncClient()` 进行 HTTP 请求
- 使用 Pydantic 模型进行数据验证

### 错误处理
- 捕获 `httpx.TimeoutException` 处理超时
- 捕获 `httpx.HTTPStatusError` 处理 HTTP 错误
- 提供友好的错误消息
- 记录详细的错误日志

### API 集成
- NWS API 基础 URL: `https://api.weather.gov`
- 预警 API: `/alerts/active?area={state}`
- 预报 API: `/points/{lat},{lon}` 然后获取 `forecast` URL

### 代码风格
- 使用中文注释和文档字符串
- 遵循 PEP 8 代码风格
- 使用类型注解
- 保持函数简洁明确

## 更多信息

您可以在以下链接找到更多信息和示例：
- https://modelcontextprotocol.io/llms-full.txt
- https://github.com/modelcontextprotocol/create-python-server
