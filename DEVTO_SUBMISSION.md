# DEV.to Gemma 4 Challenge — Submission Draft

## Title
**Tobor Voice Mirror: Using Gemma 4 as the Interpretive Core of a Performance Art Robot**

## Tags
`gemma4` `ollama` `python` `ai` `opensource`

---

## Short description (tagline)

> A small poetic AI instrument. Tobor listens. Gemma 4 reads. The mirror responds.

---

## The Project

Tobor is a physical performance robot built for live art around intergenerational memory and human connection. In performance, a person speaks — about family, grief, longing, things left unsaid — and Tobor responds not with words, but with light, color, and body movement.

For this challenge, I built the **interpretive layer**: the part where voice becomes expressive response.

```
Voice → Whisper (local STT) → Gemma 4 (relational reading) → Canvas visuals + Robot movement
```

Gemma 4 is the **only AI model** in the chain. It receives a spoken utterance and returns a structured relational state — not a label, but a reading: what the person is really expressing, at what intensity, with what quality of energy.

---

## What Gemma 4 Actually Does

The system prompt is the heart of the project. It frames Gemma not as a classifier, but as an empathic presence:

```
You are the empathic core of Tobor — a performance robot that witnesses human stories.

Listen to what is said. Beneath the words, find:
- The relational undercurrent
- What it costs the speaker to say this
- What they need to be seen

Respond ONLY with a valid JSON object.
```

Given this utterance:
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

The canvas blooms with fractured amber-lavender light. Tobor leans forward. The word *unspoken* appears at the center of the screen and slowly dissolves.

---

## Why Gemma 4 Specifically

**1. Local inference is not optional — it's the point.**

Tobor performs in community centers, care homes, family living rooms, school gyms. No reliable wifi. No cloud. The things people say in performance are private and personal — they should never leave the room.

With `gemma4:2b` running on a Raspberry Pi 5, the entire system operates offline. No API keys. No data sent anywhere. No latency from network calls.

**2. Gemma 4 reads between the lines.**

Tone-labeling models trained on labeled datasets only reach the surface of language. Gemma 4 understands that *"I'm fine"* said after *"my father never came to my shows"* means something specific. It finds cost, ambivalence, what is carried — which is exactly what an expressive art installation needs to respond to.

**3. Structured output that holds in real time.**

Gemma 4's instruction-following is precise enough to return clean, validated JSON reliably in a live performance loop. It becomes the control brain of the system — not just a conversational interface.

---

## The Visualization

The browser canvas is dark. At its center, an orb breathes — slowly, audibly slow — its color, pulse speed, and surrounding particle field all driven by Gemma's reading.

- `vulnerable` → scattered pale blue light, barely moving, robot still
- `fierce` → orange-red particles bursting outward, robot reaching
- `warm` → expanding golden glow, robot arms open
- `tense` → crimson field pulling inward, micro-jitter

The `resonance` field — the single word Gemma chooses to name what is really being expressed — appears at the center of the orb and fades.

---

## Running It

```bash
ollama pull gemma4:4b
pip install -r requirements.txt

# Text mode — no microphone needed
python tobor.py

# Open http://localhost:5000 and type:
# > I stayed too long. I knew it and I stayed anyway.
```

Or for a quick terminal demo:
```bash
python examples/demo.py
```

---

## Why This Matters

The question behind Tobor is: *what does it mean for a machine to witness human pain and reflect it back — without judgment, without diagnosis, without storing anything?*

With Gemma 4 running locally, the answer becomes: a machine can do this anywhere, for anyone, with complete privacy. The expressive response happens in the room and stays in the room.

That feels like the right use of a local language model.

---

## Repository

[github.com/vjzanne/tobor-gemma-voice](https://github.com/vjzanne/tobor-gemma-voice)

**Stack:** Python · Gemma 4 (Ollama) · faster-whisper · Flask-SocketIO · HTML5 Canvas

---
