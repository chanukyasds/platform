import os


PLATFORM_API_URL = os.getenv(
    "PLATFORM_API_URL",
    "http://localhost:8000",
).rstrip("/")

MCP_PUBLIC_HOST = os.getenv(
    "MCP_PUBLIC_HOST",
    "localhost",
)

MCP_PUBLIC_ORIGIN = os.getenv(
    "MCP_PUBLIC_ORIGIN",
    "http://localhost",
)