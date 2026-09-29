from pathlib import Path

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

BASE_DIR = Path(__file__).resolve().parent.parent


TARGET_FOLDER =[
    str(BASE_DIR/"projectworkspace"),
   
]
server_params=StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@modelcontextprotocol/server-filesystem",
         *TARGET_FOLDER,
    ],
)

connection_params =StdioConnectionParams(server_params=server_params,timeout=200)
mcp_tools=McpToolset(connection_params=connection_params)

# Read only file system access - for reviewer

reviewer_mcp_tools=McpToolset(
     connection_params=connection_params,
     tool_filter=[
         "read_file",
         "read_text_file",
         "read_multiple_files",
         "list_directory",
         "list_directory",
         "list_directory_with_sizes",
         "directory_tree",
         "search_files",
         "get_file_info",
     ],
)