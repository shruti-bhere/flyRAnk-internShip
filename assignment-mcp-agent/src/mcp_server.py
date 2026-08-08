"""
MCP (Model Context Protocol) Primitive Demo:
Exposing a local file reader tool to an AI Client.
"""
import os
import json

def read_local_file(filepath: str) -> str:
    """Tool: Reads content from local system file (Chat alone cannot do this)."""
    if not os.path.exists(filepath):
        return json.dumps({"error": "File not found"})
    
    with open(filepath, "r", encoding="utf-8") as f:
        data = f.read()
    return json.dumps({"content": data})

def execute_mcp_tool(tool_name: str, arguments: dict):
    """MCP Host primitive router."""
    if tool_name == "read_local_file":
        return read_local_file(arguments.get("filepath"))
    raise ValueError(f"Unknown tool: {tool_name}")

if __name__ == "__main__":
    # Test execution simulating an MCP Client tool call
    result = execute_mcp_tool("read_local_file", {"filepath": "docs/EXPLAINER.md"})
    print("MCP Tool Output:", result[:100], "...")