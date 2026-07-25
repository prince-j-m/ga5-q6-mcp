import hashlib

from mcp.server.fastmcp import FastMCP, Context

EMAIL = "23f3001847@ds.study.iitm.ac.in".strip().lower()

mcp = FastMCP(
    "IITM GA5 MCP",
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
async def solve_challenge(ctx: Context) -> str:
    # Read headers from the incoming HTTP request
    challenge = ctx.headers.get("x-exam-challenge", "")

    result = hashlib.sha256(
        f"{challenge}:{EMAIL}".encode("utf-8")
    ).hexdigest()[:16]

    return result


app = mcp.streamable_http_app()