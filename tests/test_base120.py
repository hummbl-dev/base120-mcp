"""Tests for base120-mcp mental models and server."""

from base120_mcp import Base120MCPServer, MODELS


def test_models_exist():
    assert len(MODELS) >= 15
    assert "IN1" in MODELS
    assert "SY1" in MODELS


def test_base120_search():
    server = Base120MCPServer()
    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "base120_search", "arguments": {"query": "inversion"}},
    }
    resp = server.handle_request(req)
    assert resp["result"]["isError"] is False
    assert "Inversion" in resp["result"]["content"][0]["text"]


def test_base120_apply():
    server = Base120MCPServer()
    req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "base120_apply",
            "arguments": {
                "model_id": "IN1",
                "problem_statement": "Deploying an autonomous agent to production database",
            },
        },
    }
    resp = server.handle_request(req)
    assert resp["result"]["isError"] is False
    text = resp["result"]["content"][0]["text"]
    assert "Applying Base120 Model: [IN1] Inversion" in text
