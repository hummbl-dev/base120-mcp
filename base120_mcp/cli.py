"""Interactive CLI and Terminal REPL for Base120 Mental Models."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional
from .models import MODELS, MentalModel

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def print_banner() -> None:
    print(f"""{CYAN}{BOLD}
╔═══════════════════════════════════════════════════════════════╗
║   HUMMBL BASE120 — Cognitive Mental Models Architecture       ║
║   120 Verified Reasoning Models across 6 Transformations      ║
╚═══════════════════════════════════════════════════════════════╝{RESET}
""")


def display_model(m: MentalModel) -> None:
    print(f"\n{BOLD}{CYAN}[{m.id}] {m.name}{RESET} {DIM}({m.domain} / {m.transformation}){RESET}")
    print(f"{BOLD}Definition:{RESET} {m.definition}")
    print(f"{BOLD}Prompt Application:{RESET} {GREEN}{m.prompt_guidance}{RESET}\n")


def cmd_search(query: str) -> None:
    q = query.lower()
    matches: List[MentalModel] = []
    for m in MODELS.values():
        if q in m.id.lower() or q in m.name.lower() or q in m.transformation.lower() or q in m.domain.lower() or q in m.definition.lower():
            matches.append(m)

    if not matches:
        print(f"{YELLOW}No mental models found matching '{query}'.{RESET}")
        return

    print(f"\n{BOLD}Found {len(matches)} matching Base120 models:{RESET}")
    for m in matches:
        print(f"  {CYAN}{BOLD}{m.id:5}{RESET} {m.name:32} {DIM}({m.domain}){RESET} — {m.definition[:70]}...")


def cmd_get(model_id: str) -> None:
    m_id = model_id.upper()
    if m_id not in MODELS:
        print(f"{YELLOW}Unknown model ID '{model_id}'. Try 'base120 search <term>' or 'base120 list'.{RESET}")
        return
    display_model(MODELS[m_id])


def cmd_list(family: Optional[str] = None) -> None:
    families = ["P", "IN", "CO", "DE", "RE", "SY"]
    target_families = [family.upper()] if family and family.upper() in families else families

    for fam in target_families:
        fam_models = [m for m in MODELS.values() if m.transformation == fam]
        d_name = fam_models[0].domain if fam_models else fam
        print(f"\n{BOLD}{PURPLE}=== Transformation [{fam}]: {d_name} ({len(fam_models)} Models) ==={RESET}")
        for m in fam_models:
            print(f"  {CYAN}{m.id:5}{RESET} {m.name:32} — {DIM}{m.definition[:65]}...{RESET}")


def cmd_chain(model_ids: List[str], problem: str) -> None:
    valid_models: List[MentalModel] = []
    for m_id in model_ids:
        mid = m_id.upper()
        if mid in MODELS:
            valid_models.append(MODELS[mid])
        else:
            print(f"{YELLOW}Warning: Model '{m_id}' not found, skipping.{RESET}")

    if not valid_models:
        print(f"{YELLOW}No valid models provided for chaining.{RESET}")
        return

    print(f"\n{BOLD}{CYAN}=== Base120 Composite Reasoning Chain ==={RESET}")
    print(f"{BOLD}Problem Statement:{RESET} {problem}\n")
    print(f"{BOLD}Active Models:{RESET}")
    for i, m in enumerate(valid_models, 1):
        print(f"  {i}. {BOLD}[{m.id}] {m.name}{RESET} ({m.domain}): {m.definition}")

    print(f"\n{BOLD}{GREEN}Composite Reasoning Protocol:{RESET}")
    for i, m in enumerate(valid_models, 1):
        print(f"  Step {i} ({m.name}): Evaluate '{problem}' through the lens of {m.name}. {m.prompt_guidance}")


def repl() -> None:
    print_banner()
    print("Type 'search <term>', 'get <id>', 'list [family]', 'chain <id1> <id2> <problem>', or 'exit'\n")
    while True:
        try:
            line = input(f"{CYAN}base120>{RESET} ").strip()
            if not line:
                continue
            if line.lower() in ("exit", "quit", "q"):
                break
            parts = line.split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if cmd == "search":
                cmd_search(arg)
            elif cmd == "get":
                cmd_get(arg)
            elif cmd == "list":
                cmd_list(arg or None)
            elif cmd == "chain":
                chain_parts = arg.split(maxsplit=2)
                if len(chain_parts) >= 3:
                    cmd_chain([chain_parts[0], chain_parts[1]], chain_parts[2])
                else:
                    print("Usage: chain <model1> <model2> <problem_statement>")
            else:
                # Default search if bare word
                cmd_search(line)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Base120 REPL.")
            break


def main() -> None:
    parser = argparse.ArgumentParser(description="Base120 Mental Models CLI & Reasoning Engine")
    subparsers = parser.add_subparsers(dest="command")

    # search
    p_search = subparsers.add_parser("search", help="Search mental models by keyword")
    p_search.add_argument("query", help="Search keyword")

    # get
    p_get = subparsers.add_parser("get", help="Get full prompt guidance for a model ID")
    p_get.add_argument("id", help="Model ID (e.g. P1, IN2, SY4)")

    # list
    p_list = subparsers.add_parser("list", help="List models by family")
    p_list.add_argument("family", nargs="?", default=None, help="Family code (P, IN, CO, DE, RE, SY)")

    # chain
    p_chain = subparsers.add_parser("chain", help="Compose multiple models into a reasoning chain")
    p_chain.add_argument("models", nargs="+", help="Model IDs to compose (e.g. IN1 P1)")
    p_chain.add_argument("--problem", "-p", required=True, help="Problem statement to analyze")

    # repl
    subparsers.add_parser("repl", help="Start interactive terminal REPL")

    args = parser.parse_args()

    if not args.command or args.command == "repl":
        repl()
    elif args.command == "search":
        cmd_search(args.query)
    elif args.command == "get":
        cmd_get(args.id)
    elif args.command == "list":
        cmd_list(args.family)
    elif args.command == "chain":
        cmd_chain(args.models, args.problem)


if __name__ == "__main__":
    main()
