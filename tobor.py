#!/usr/bin/env python3
"""
tobor-gemma-voice
=================
A small poetic AI instrument powered by Gemma 4.

Tobor listens. Gemma interprets. The mirror responds.

Usage:
  python tobor.py                          # text mode, browser visualizer
  python tobor.py --mode mic               # live microphone
  python tobor.py --mode text --no-server  # console only, no browser
  python tobor.py --model gemma4:4b        # larger model (requires GPU)
"""

import argparse
import sys
import threading


def main():
    parser = argparse.ArgumentParser(
        description="Tobor Voice Mirror — expressive translation via Gemma 4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--mode", choices=["text", "mic"], default="text",
        help="Input: 'text' to type, 'mic' for microphone (default: text)",
    )
    parser.add_argument(
        "--model", default="gemma4:2b",
        help="Ollama model name (default: gemma4:2b)",
    )
    parser.add_argument(
        "--port", type=int, default=5000,
        help="Web visualizer port (default: 5000)",
    )
    parser.add_argument(
        "--no-server", action="store_true",
        help="Disable web visualizer — print to console only",
    )
    parser.add_argument(
        "--language", choices=["en", "nl"], default="en",
        help="Speech language for mic mode (default: en)",
    )
    args = parser.parse_args()

    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║   T O B O R   V O I C E              ║")
    print("  ║   emotional mirror · powered by Gemma ║")
    print("  ╚══════════════════════════════════════╝")
    print()

    # ── Interpreter ──────────────────────────────────────────
    from src.interpreter import GemmaInterpreter
    interpreter = GemmaInterpreter(model=args.model)

    if not interpreter.check_connection():
        print(f"  WARNING: Ollama not reachable or model '{args.model}' not found.")
        print(f"  To install: ollama pull {args.model}")
        print(f"  Falling back to keyword-based interpretation.\n")
    else:
        print(f"  Gemma  : {args.model} ✓")

    print(f"  Mode   : {args.mode}")

    # ── Visualizer server ────────────────────────────────────
    server = None
    if not args.no_server:
        try:
            from src.server import VisualizerServer
            server = VisualizerServer(port=args.port)
            threading.Thread(target=server.run, daemon=True).start()
            print(f"  Visual : http://localhost:{args.port}")
        except Exception as e:
            print(f"  [warn] Could not start visualizer: {e}")
            print(f"         Install with: pip install flask flask-socketio")

    # ── Robot bridge ─────────────────────────────────────────
    try:
        from src.robot_bridge import apply_state as robot_apply
    except Exception:
        robot_apply = lambda _: None

    print()
    print("  Tobor is listening...\n")
    print("  " + "─" * 46)

    # ── Utterance handler ────────────────────────────────────
    def on_utterance(text: str):
        if not text.strip():
            return

        short = text[:80] + ("..." if len(text) > 80 else "")
        print(f"\n  Voice   : \"{short}\"")
        print("  Gemma   : interpreting...", end="", flush=True)

        state = interpreter.interpret(text)

        print(
            f"\r  Gemma   : {state['emotion']:12s}"
            f"  intensity={state['intensity']:.2f}"
            f"  energy={state['energy']:.2f}"
        )
        print(
            f"  Resonate: {state['resonance']:16s}"
            f"  mode={state['visual_mode']}"
        )
        print(f"  Robot   : {state['robot_state']}")
        print("  " + "─" * 46)

        if server:
            server.broadcast(state)

        robot_apply(state["robot_state"])

    # ── Run ───────────────────────────────────────────────────
    if args.mode == "mic":
        try:
            from src.listener import VoiceListener
            listener = VoiceListener(language=args.language, on_utterance=on_utterance)
            listener.run()
        except RuntimeError as e:
            print(f"\n  ERROR: {e}\n")
            sys.exit(1)
    else:
        _text_mode(on_utterance)


def _text_mode(callback):
    print("  Type something to interpret. Press Ctrl+C to exit.\n")
    try:
        while True:
            try:
                text = input("  > ")
                if text.strip():
                    callback(text)
            except EOFError:
                break
    except KeyboardInterrupt:
        print("\n\n  Tobor goes quiet.\n")


if __name__ == "__main__":
    main()
