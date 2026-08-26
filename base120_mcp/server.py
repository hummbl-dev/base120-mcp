"""Model Context Protocol (MCP) Server exposing 120 Canonical Base120 Mental Models."""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional
from .models import MODELS, MentalModel


class Base120MCPServer:
    """Zero-dependency MCP Server for Base120 Mental Models."""

    def __init__(self) -> None:
        self.name = "base120-mcp"
        self.version = "0.1.0"

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": self.name, "version": self.version},
                    "capabilities": {"tools": {"listChanged": True}},
                },
            }

        if method == "notifications/initialized" or method == "ping":
            return {"jsonrpc": "2.0", "id": req_id, "result": {}}

        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {
                            "name": "base120_search",
                            "description": "Search Base120 mental models by keyword or transformation (Perspective, Inversion, Composition, Decomposition, Recursion, Systems).",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string", "description": "Search term or concept (e.g. 'premortem', 'first principles', 'inversion', 'variety')"},
                                },
                                "required": ["query"],
                            },
                        },
                        {
                            "name": "base120_apply",
                            "description": "Get structured reasoning guidance for applying a specific mental model to an engineering or strategic problem.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "model_id": {"type": "string", "description": "Model ID (e.g. 'P1', 'IN2', 'CO1', 'DE1', 'RE1', 'SY4')"},
                                    "problem_statement": {"type": "string", "description": "The specific engineering or architectural challenge to evaluate"},
                                },
                                "required": ["model_id", "problem_statement"],
                            },
                        },
                    ]
                },
            }

        if method == "tools/call":
            name = params.get("name")
            args = params.get("arguments", {})

            if name == "base120_search":
                q = args.get("query", "").lower()
                matches = []
                for m in MODELS.values():
                    if q in m.id.lower() or q in m.name.lower() or q in m.transformation.lower() or q in m.domain.lower() or q in m.definition.lower():
                        matches.append({
                            "id": m.id,
                            "name": m.name,
                            "transformation": m.transformation,
                            "domain": m.domain,
                            "definition": m.definition
                        })
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(matches, indent=2)}], "isError": False},
                }

            if name == "base120_apply":
                m_id = args.get("model_id", "").upper()
                problem = args.get("problem_statement", "")
                if m_id not in MODELS:
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {"content": [{"type": "text", "text": f"Unknown model ID: {m_id}. Try searching with base120_search."}], "isError": True},
                    }
                m = MODELS[m_id]
                guidance = f"### Base120 Model: [{m.id}] {m.name} ({m.domain} / {m.transformation})\n\n**Definition**: {m.definition}\n\n**Problem Evaluated**: {problem}\n\n**Reasoning Application**:\n{m.prompt_guidance}"
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": guidance}], "isError": False},
                }

        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

    def run_stdio(self) -> None:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
                resp = self.handle_request(req)
                if resp:
                    sys.stdout.write(json.dumps(resp) + "\n")
                    sys.stdout.flush()
            except json.JSONDecodeError:
                pass
