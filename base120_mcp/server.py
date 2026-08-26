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
                        {
                            "name": "base120_chain",
                            "description": "Compose 2-3 Base120 mental models into a structured, step-by-step reasoning chain for a complex problem.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "model_ids": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Array of 2-3 model IDs (e.g. ['IN2', 'P1', 'SY4'])",
                                    },
                                    "problem_statement": {"type": "string", "description": "The complex problem to analyze across the model chain"},
                                },
                                "required": ["model_ids", "problem_statement"],
                            },
                        },
                        {
                            "name": "base120_list",
                            "description": "List all mental models within a specific transformation family (P, IN, CO, DE, RE, SY).",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "transformation": {
                                        "type": "string",
                                        "enum": ["P", "IN", "CO", "DE", "RE", "SY", "ALL"],
                                        "description": "Transformation family code (P, IN, CO, DE, RE, SY, or ALL)",
                                    }
                                },
                                "required": ["transformation"],
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
                            "definition": m.definition,
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

            if name == "base120_chain":
                m_ids = args.get("model_ids", [])
                problem = args.get("problem_statement", "")
                valid_models = [MODELS[m.upper()] for m in m_ids if m.upper() in MODELS]
                if not valid_models:
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {"content": [{"type": "text", "text": "No valid model IDs provided for chaining."}], "isError": True},
                    }

                chain_text = f"### Base120 Composite Reasoning Chain\n\n**Problem Statement**: {problem}\n\n**Active Models**:\n"
                for i, vm in enumerate(valid_models, 1):
                    chain_text += f"{i}. [{vm.id}] {vm.name} ({vm.domain}): {vm.definition}\n"
                chain_text += "\n**Step-by-Step Chain Execution**:\n"
                for i, vm in enumerate(valid_models, 1):
                    chain_text += f"- **Step {i} ({vm.name})**: {vm.prompt_guidance}\n"

                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": chain_text}], "isError": False},
                }

            if name == "base120_list":
                tf = args.get("transformation", "ALL").upper()
                if tf == "ALL":
                    res = [{"id": m.id, "name": m.name, "transformation": m.transformation, "domain": m.domain} for m in MODELS.values()]
                else:
                    res = [{"id": m.id, "name": m.name, "transformation": m.transformation, "domain": m.domain} for m in MODELS.values() if m.transformation == tf]
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}], "isError": False},
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
