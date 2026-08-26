"""Tests for Base120 reasoning chain and family listing tools."""

from base120_mcp import Base120MCPServer


def test_base120_chain():
    server = Base120MCPServer()
    req = {
        "jsonrpc": "2.0",
        "id": 10,
        "method": "tools/call",
        "params": {
            "name": "base120_chain",
            "arguments": {
                "model_ids": ["IN2", "P1", "SY4"],
                "problem_statement": "Preventing cascading agent task failures in production",
            },
        },
    }
    resp = server.handle_request(req)
    assert resp["result"]["isError"] is False
    text = resp["result"]["content"][0]["text"]
    assert "Premortem Analysis" in text
    assert "First Principles" in text
    assert "Requisite Variety" in text


def test_base120_list():
    server = Base120MCPServer()
    req = {
        "jsonrpc": "2.0",
        "id": 11,
        "method": "tools/call",
        "params": {"name": "base120_list", "arguments": {"transformation": "IN"}},
    }
    resp = server.handle_request(req)
    assert resp["result"]["isError"] is False
    assert "Subtractive Thinking" in resp["result"]["content"][0]["text"]
    assert "Premortem Analysis" in resp["result"]["content"][0]["text"]
