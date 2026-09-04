# AGENTS.md — base120-mcp

## Project

**base120-mcp** — 120 validated mental models packaged as an MCP server to upgrade reasoning, prompt engineering, and architectural decisions in Claude Desktop, Cursor, and Windsurf.**.

## Scope

- In scope: Core implementation, documentation, configuration, and tests for base120-mcp.
- Out of scope: Unreviewed upstream changes, unverified external dependencies, direct pushes to main.

## Governance & Behavioral DNA

This repository adheres to the HUMMBL Agent Fleet governance standards:
- Canonical agent contracts and governance rules derive from `.agents` and `apex-nexus`.
- Agents operating in this repository must follow the Crab Protocol and Bus Protocol where applicable.
- No runtime data or credentials in git: keep history, caches, and auth tokens out of version control.
- Conventional Commits required for all commits (`feat:`, `fix:`, `chore:`, `docs:`, etc.).
- Work must be performed on dedicated branches; direct pushes to `main` without review are prohibited.

## Conventions

- Branch naming: `type/agent/short-desc` (e.g., `chore/agent/governance-baseline`).
- Adhere to the zero-drift policy: keep configuration and contract copies synchronized with canonical definitions.
