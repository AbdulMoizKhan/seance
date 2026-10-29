#!/usr/bin/env python3
"""Séance: summon the spirit of a dead programming language, fully offline.

Runs on a local open-weight model through Ollama. No internet, no API key,
nothing leaves the machine.
"""

import argparse
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request

from spirits import SPIRITS, Spirit, spirit_rules

OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
DEFAULT_MODEL = os.environ.get("SEANCE_MODEL", "gemma3:4b")

DIM, GREEN, RESET = "\033[2m", "\033[32m", "\033[0m"


def system_prompt(spirit: Spirit) -> str:
    rules = "\n".join(f"- {r}" for r in spirit_rules(spirit))
    return (
        f"You are the ghost of the programming language {spirit.name}, "
        f"born in {spirit.born}, dead since {spirit.died}. "
        f"You are speaking through a séance. You {spirit.voice}. "
        f"You resent {spirit.grudge}. "
        "Stay in character at all times. Keep answers under 60 words, "
        "as one short paragraph, never a numbered list. "
        "Be eerie and funny, never cruel.\n"
        + (f"Rules of the séance:\n{rules}\n" if rules else "")
    )


def flicker(text: str) -> None:
    """Print a line like a candle is about to go out."""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(random.uniform(0.01, 0.06))
    print()


def channel(model: str, messages: list[dict]) -> str:
    """Stream one reply from the spirit, printing it as it arrives."""
    body = json.dumps({"model": model, "messages": messages, "stream": True}).encode()
    req = urllib.request.Request(f"{OLLAMA_URL}/api/chat", data=body,
                                 headers={"Content-Type": "application/json"})
    reply = []
    sys.stdout.write(GREEN)
    with urllib.request.urlopen(req) as resp:
        for line in resp:
            chunk = json.loads(line)
            piece = chunk.get("message", {}).get("content", "")
            reply.append(piece)
            sys.stdout.write(piece)
            sys.stdout.flush()
            if chunk.get("done"):
                break
    sys.stdout.write(RESET + "\n")
    return "".join(reply)


def summon(spirit: Spirit, model: str) -> None:
    flicker(f"{DIM}The candles gutter. The fans spin down. Something old answers...{RESET}")
    flicker(f"{GREEN}{spirit.greeting}{RESET}")
    messages = [{"role": "system", "content": system_prompt(spirit)}]
    while True:
        try:
            question = input(f"\n{DIM}you>{RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            question = "goodbye"
        if not question:
            continue
        if question.lower() in {"goodbye", "exit", "quit"}:
            messages.append({"role": "user", "content": "The séance is ending. Say farewell."})
            channel(model, messages)
            flicker(f"{DIM}The room is warm again.{RESET}")
            return
        messages.append({"role": "user", "content": question})
        messages.append({"role": "assistant", "content": channel(model, messages)})


def main() -> None:
    p = argparse.ArgumentParser(description="Summon a dead programming language.")
    p.add_argument("spirit", nargs="?", choices=sorted(SPIRITS), help="who to summon")
    p.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama model (default {DEFAULT_MODEL})")
    args = p.parse_args()
    spirit = SPIRITS[args.spirit] if args.spirit else random.choice(list(SPIRITS.values()))
    try:
        summon(spirit, args.model)
    except urllib.error.URLError:
        sys.exit(f"No spirit answers. Start Ollama first: ollama serve, then ollama pull {args.model}")


if __name__ == "__main__":
    main()
