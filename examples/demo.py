#!/usr/bin/env python3
"""
Tobor Gemma Voice — Quick Demo
================================
No microphone. No browser. No hardware.
Tests Gemma 4 expressive translation directly from the terminal.

Usage:
  python examples/demo.py
  python examples/demo.py --model gemma4:2b
  python examples/demo.py --interactive
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.interpreter import GemmaInterpreter

SAMPLES = [
    "I never told my mother I was angry at her. She died before I could say it.",
    "My hands shake when I think about going back home.",
    "There's this moment in every song where I feel like everything might be okay.",
    "I don't understand why it still hurts. It was so long ago.",
    "When he left, I thought — finally. And then I cried for three days.",
    "Sometimes I pretend to be fine just to give everyone a break from me.",
    "She used to sing that to me when I was scared. I haven't heard it since she died.",
    "I am tired. Not sleepy tired. Something deeper.",
    "I thought if I worked hard enough I could fix it. I couldn't.",
    "He never said he was proud of me. Not once. And I keep doing things anyway.",
]


def run_samples(interpreter):
    print("  " + "─" * 60)
    for utterance in SAMPLES:
        display = utterance[:72] + "..." if len(utterance) > 72 else utterance
        print(f"\n  Voice    : \"{display}\"")

        state = interpreter.interpret(utterance)

        print(
            f"  Emotion  : {state['emotion']:12s}"
            f"  intensity={state['intensity']:.2f}"
            f"  energy={state['energy']:.2f}"
        )
        print(
            f"  Resonance: {state['resonance']:14s}"
            f"  visual={state['visual_mode']}"
        )
        print(f"  Robot    : {state['robot_state']}")
        print("  " + "─" * 60)


def run_interactive(interpreter):
    print("  Type a phrase and press Enter. Ctrl+C to exit.\n")
    print("  " + "─" * 60)
    try:
        while True:
            try:
                text = input("\n  > ")
                if not text.strip():
                    continue
                state = interpreter.interpret(text)
                print(
                    f"\n  {state['emotion'].upper():12s}"
                    f"  ({state['resonance']})"
                    f"  intensity={state['intensity']:.2f}"
                    f"  energy={state['energy']:.2f}"
                )
                print(f"  visual={state['visual_mode']}   robot={state['robot_state']}")
            except EOFError:
                break
    except KeyboardInterrupt:
        print("\n")


def main():
    parser = argparse.ArgumentParser(description="Tobor Gemma demo")
    parser.add_argument("--model", default="gemma4:4b")
    parser.add_argument("--interactive", action="store_true",
                        help="Free-form input instead of sample utterances")
    args = parser.parse_args()

    print()
    print("  TOBOR · EMOTIONAL MIRROR · DEMO")
    print(f"  Model: {args.model}")
    print()

    interpreter = GemmaInterpreter(model=args.model)

    if not interpreter.check_connection():
        print(f"  NOTE: Ollama not reachable / model not found.")
        print(f"  Running keyword fallback (install Ollama for full Gemma 4 inference).\n")
        print(f"    ollama pull {args.model}\n")
    else:
        print(f"  Gemma 4 connected ✓\n")

    if args.interactive:
        run_interactive(interpreter)
    else:
        run_samples(interpreter)
        print()
        print("  Full interactive mode: python tobor.py --mode text")
        print()


if __name__ == "__main__":
    main()
