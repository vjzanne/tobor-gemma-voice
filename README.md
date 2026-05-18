# tobor-gemma-voice

**Tobor listens. Gemma 4 interprets. The mirror responds.**

Tobor is a therapy-art robot built for live performance around intergenerational trauma, grief, and human connection. When a person speaks — about memory, loss, longing, family — Tobor doesn't reply. It *reflects*. The room changes color. The robot leans forward. A single word appears and dissolves.

This repository is the interpretive layer: the part where voice becomes feeling.

---

## How It Works

```
Voice / text input
       │
       ▼
  faster-whisper       ←  local speech-to-text, no cloud
       │
       ▼
    Gemma 4            ←  the interpretive brain, runs via Ollama
       │                   reads what is really being said
       ▼
  JSON state
  ┌─────────────────────────────────────┐
  │ emotion    vulnerable               │
  │ intensity  0.87                     │
  │ energy     0.28                     │
  │ resonance  unspoken                 │
  │ visual     fragmented_glow          │
  │ robot      leaning_in               │
  └─────────────────────────────────────┘
       │
       ├──▶  Canvas visualization  (live browser)
       └──▶  Robot body             (Raspberry Pi, optional)
```

Gemma 4 is the **only AI model**. No pre-trained tone detectors. No labeled datasets. Just a language model asked to find what is really being said — and what it costs to say it.

---

## Demo (60 seconds)

```bash
# 1. Pull the model
ollama pull gemma4:4b          # or gemma4:2b for Raspberry Pi

# 2. Install
pip install -r requirements.txt

# 3. Run
python tobor.py

# 4. Open http://localhost:5000
#    Type something — anything true.
```

No microphone required. Type directly. Watch the canvas respond.

Or run the terminal demo with no browser:

```bash
python examples/demo.py
```

---

## Example

Given:
> *"I never told my mother I was angry at her. She died before I could say it."*

Gemma returns:
```json
{
  "emotion": "conflicted",
  "intensity": 0.89,
  "energy": 0.31,
  "resonance": "unspoken",
  "visual_mode": "fragmented_glow",
  "robot_state": "leaning_in"
}
```

The canvas blooms with fractured amber-lavender light. Tobor leans forward. The word *unspoken* appears and slowly dissolves.

---

## Expressive Vocabulary

Gemma reads 10 relational states, each with its own visual signature:

| Emotion | Visual | What it means |
|---------|--------|---------------|
| `tender` | soft breathing ring | gentle care, fragile |
| `vulnerable` | scattered pale light | exposed, at cost |
| `conflicted` | micro-shaking field | two true things at once |
| `warm` | expanding golden glow | love, home, safety |
| `hesitant` | barely moving | weighing something |
| `longing` | slow drift | missing what's gone |
| `tense` | inward collapse | pressure, resistance |
| `fierce` | outward burst | refusing to break |
| `absent` | intermittent sparks | numb, floating |
| `playful` | spiraling motes | lightness, relief |

---

## Why Gemma 4

**Local inference is not optional — it's the point.**

Tobor performs in community centers, care homes, school gyms, living rooms. No reliable wifi. No cloud. The stories people share are private. They should never leave the room.

With `gemma4:2b` on a Raspberry Pi 5, the entire system runs offline. No API keys. No data logging. No latency.

**Gemma 4 reads subtext.**

Tone-labeling models trained on labeled data only reach the surface. Gemma 4 understands that *"I'm fine"* said after *"my father never came to my shows"* means something specific. It finds cost, ambivalence, the gap between what was said and what was meant — which is what an empathic witness needs.

**Structured output that holds.**

Gemma 4's instruction-following is precise enough to return clean, validated JSON reliably in a real-time performance loop. It becomes a control brain, not just a chat interface.

---

## Installation

**Requirements:** Python 3.10+ · [Ollama](https://ollama.ai) running locally

```bash
git clone https://github.com/vjzanne/tobor-gemma-voice
cd tobor-gemma-voice
pip install -r requirements.txt
```

| Command | What it does |
|---------|-------------|
| `python tobor.py` | Text input + live browser visualization |
| `python tobor.py --mode mic` | Microphone input (requires faster-whisper) |
| `python tobor.py --model gemma4:2b` | Smaller model for Raspberry Pi |
| `python tobor.py --no-server` | Console output only, no browser |
| `python examples/demo.py` | Quick terminal demo |

---

## Raspberry Pi

```bash
ollama pull gemma4:2b
python tobor.py --model gemma4:2b --mode mic --language en
```

To connect Tobor's physical body, wire a PCA9685 board to the Pi's I2C bus and uncomment the hardware section in `src/robot_bridge.py`. Each relational state maps to a specific servo position — torso lean, arm height — so the robot's body expresses what Gemma hears.

---

## Structure

```
tobor-gemma-voice/
├── tobor.py              ← entry point
├── src/
│   ├── interpreter.py    ← Gemma 4 resonance engine  ← the core
│   ├── listener.py       ← microphone → faster-whisper STT
│   ├── server.py         ← Flask-SocketIO visualizer server
│   └── robot_bridge.py   ← RPi PCA9685 servo bridge (no-op on PC)
├── web/
│   └── index.html        ← canvas visualization (vanilla JS)
└── examples/
    ├── demo.py
    └── sample_utterances.txt
```

---

## About Tobor

Tobor is a performance art project built by Zanne and Pjotr. The robot has a 40-year family history — built, broken, rebuilt, reinterpreted across generations. This demo is the interpretive layer for the 2025 performances.

*What does it mean for a machine to witness human pain, and reflect it back without judgment?*

With Gemma 4 running locally, the answer is: a machine can do this anywhere, for anyone, without requiring privacy to be traded away. The stories stay in the room.

---

## License

MIT
