# tobor-gemma-voice

**Tobor transforms voice into live visual response using local AI.**

This project explores how a small local language model can act as an interpretive layer between human speech and real-time audiovisual expression.

A person speaks.
The system does not interpret in a clinical or diagnostic sense.
It translates language into a structured emotional state that drives visuals and optional robotic movement.

---

## What this is

Tobor is an experimental audiovisual instrument.

It sits between:

* spoken language (or text input)
* a local language model (Gemma 4)
* real-time visual and physical output

The goal is not analysis or classification.
The goal is translation: from language → expressive state → movement.

---

## System flow

```
Voice / text input
        │
        ▼
faster-whisper (optional)
speech-to-text, local
        │
        ▼
Gemma 4 (Ollama)
interprets meaning + tone in context
        │
        ▼
structured JSON state
        │
        ├──► browser visualization (live canvas)
        └──► robot control (optional Raspberry Pi)
```

Gemma is the only reasoning component.
No emotion classifiers. No training on labeled datasets.
Only a language model responding to structured prompts.

---

## Output format

The model returns a small structured state:

```json
{
  "emotion": "vulnerable",
  "intensity": 0.82,
  "energy": 0.41,
  "resonance": "distance",
  "visual_mode": "soft_fragmentation",
  "robot_state": "leaning_in"
}
```

This is not a psychological diagnosis.
It is a control signal for an expressive system.

---

## Demo

Run without microphone:

```bash
ollama pull gemma4:4b
pip install -r requirements.txt
python tobor.py
```

Open:

```
http://localhost:5000
```

Type a sentence. The system responds visually.

---

Terminal-only version:

```bash
python examples/demo.py
```

---

## Example interaction

Input:

> I keep thinking about things I should have said.

Output:

```json
{
  "emotion": "reflective",
  "intensity": 0.73,
  "energy": 0.38,
  "resonance": "unfinished",
  "visual_mode": "slow_drift",
  "robot_state": "still"
}
```

The system responds with slow motion, muted light shifts, and reduced movement intensity.

---

## Design vocabulary

The system maps interpretation states to visual behavior:

* **tender** → soft continuous motion
* **vulnerable** → unstable or fragmented light
* **conflicted** → competing visual forces
* **warm** → expanding stable glow
* **hesitant** → delayed or reduced motion
* **longing** → slow outward drift
* **tense** → contraction and resistance
* **fierce** → sharp energetic bursts
* **absent** → minimal or fading signal
* **playful** → circular or oscillating motion

These are not psychological categories.
They are animation controls.

---

## Why Gemma 4

This project uses local AI intentionally.

Gemma 4 is used because:

* it runs locally (no cloud dependency)
* it responds fast enough for real-time interaction
* it can reliably produce structured outputs (JSON)
* it can run on small devices (including Raspberry Pi setups)

This enables the system to function in private or offline environments.

No data leaves the machine.

---

## Installation

Requirements:

* Python 3.10+
* Ollama running locally

```bash
git clone https://github.com/vjzanne/tobor-gemma-voice
cd tobor-gemma-voice
pip install -r requirements.txt
```

Run:

```bash
python tobor.py
```

Optional microphone mode:

```bash
python tobor.py --mode mic
```

Lightweight demo:

```bash
python examples/demo.py
```

---

## Raspberry Pi mode (optional)

```bash
ollama pull gemma4:2b
python tobor.py --model gemma4:2b
```

Robot output is optional and can be disabled.

---

## Project structure

```
tobor-gemma-voice/
├── tobor.py
├── src/
│   ├── interpreter.py   ← Gemma 4 interface
│   ├── listener.py      ← optional microphone input
│   ├── server.py        ← web socket bridge
│   └── robot_bridge.py  ← hardware output (optional)
├── web/
│   └── index.html       ← live visualization
├── examples/
│   ├── demo.py
│   └── sample_utterances.txt
└── README.md
```

---

## Concept

Tobor is not a conversational agent.

It is a translation system between:

* human expression
* machine interpretation
* visual/physical response

It treats language as signal rather than instruction.

The result is an expressive system that reacts in real time without trying to “understand” people in a human sense.

---

## License

MIT

