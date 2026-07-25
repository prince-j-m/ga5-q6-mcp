import hashlib

from fastapi import FastAPI
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

EMAIL = "23f3001847@ds.study.iitm.ac.in".strip().lower()

mcp = FastMCP("IITM GA5 MCP")


@mcp.tool()
async def solve_challenge() -> str:
    headers = get_http_headers()
    challenge = headers.get("x-exam-challenge", "")

    return hashlib.sha256(
        f"{challenge}:{EMAIL}".encode("utf-8")
    ).hexdigest()[:16]


# Create FastAPI app
app = FastAPI()


# Root route for grader URL check
@app.get("/")
def home():
    return {"status": "ok"}


# Mount MCP endpoint
app.mount(
    "/mcp",
    mcp.http_app(
        stateless_http=True,
        json_response=True,
    )
)