"""Tests for base120-mcp canonical 120 mental models dataset and MCP server."""

from base120_mcp import Base120MCPServer, MODELS


def test_models_count_and_families():
    assert len(MODELS) == 120
    families = set(m.transformation for m in MODELS.values())
    assert families == {"P", "IN", "CO", "DE", "RE", "SY"}


def test_base120_search_canonical():
    server = Base120MCPServer()
    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "base120_search", "arguments": {"query": "premortem"}},
    }
    resp = server.handle_request(req)
    assert resp["result"]["isError"] is False
    assert "Premortem Analysis" in resp["result"]["content"][0]["text"]


def test_base120_apply_canonical():
    server = Base120MCPServer()
    req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "base120_apply",
            "arguments": {
                "model_id": "IN2",
                "problem_statement": "Deploying an autonomous multi-agent fleet to production",
            },
        },
    }
    resp = server.handle_request(req)
    assert resp["result"]["isError"] is False
    text = resp["result"]["content"][0]["text"]
    assert "[IN2] Premortem Analysis" in text
    assert "Inversion" in text


def test_notification_gets_no_response():
    """JSON-RPC notifications (no id) must not produce a response."""
    server = Base120MCPServer()
    req = {"jsonrpc": "2.0", "method": "notifications/initialized"}
    resp = server.handle_request(req)
    assert resp == {}  # Empty dict is falsy — run_stdio skips writing it


def test_ping_gets_response():
    """ping is a request (with id) and must produce a response."""
    server = Base120MCPServer()
    req = {"jsonrpc": "2.0", "id": 99, "method": "ping"}
    resp = server.handle_request(req)
    assert resp["id"] == 99
    assert resp["result"] == {}
