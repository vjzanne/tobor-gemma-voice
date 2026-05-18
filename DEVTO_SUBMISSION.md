# DEV.to Gemma 4 Challenge — Final Submission
# Copy-paste this directly into DEV.to (Markdown editor)
# Tags: gemma, ai, opensource, showdev
# Cover image: use a photo of Tobor from /TOBOR/04_OUTREACH/Applications/FILE_2026/FILE_2026_media/tobor_hero_shot.jpg
---

# Meet Tobor: I Gave Our 40-Year-Old Family Robot a Local AI Brain with Gemma 4

*A three-generation project. A performance robot. A mindfulness guru running entirely offline.*

*This is a submission for the [Gemma 4 Challenge: Build with Gemma 4](https://dev.to/challenges/google-gemma-2026-05-06)*

> **TL;DR** — I gave my family's 40-year-old robot a brain using Gemma 4 E2B running locally on a Raspberry Pi 5. He now generates personalized mindfulness meditations based on visitors' voices, fully offline, at festivals with no WiFi. [Try the open-source demo →](https://github.com/vjzanne/tobor-gemma-voice)

---

In the 1980s, my father started building a robot to teach me electronics. He never finished it.

Forty years later, my son and I completed it together.

His name is Tobor. He dances, talks, leads guided meditations, and — his signature move — *scans* audience members through a wearable "learning hat," absorbs their voice and interests, and then delivers a workshop in their exact style. At the end, he always claims he is a better version of the person he just absorbed.

![Mirza Bekirovic's handwritten robot sketches and components from the 1980s — the unfinished build that became Tobor forty years later](INSERT-father-sketches-1980s.jpg)

---

## What I Built

Tobor is a 40-year-old family robot, originally started by my father in the 1980s and completed by my son and me in the 2020s. He performs at festivals, museums, and cultural events across the Netherlands — dancing, talking, and leading guided meditations. His signature feature is the **Knowledge Transfer Ritual**: a visitor puts on a wearable "learning hat," speaks for 60 seconds about something they know, and within moments Tobor is delivering a personalized workshop in their voice and style.

For this challenge, I extracted Tobor's AI interpretation layer into a standalone open-source project: **tobor-gemma-voice**. It demonstrates how Gemma 4 acts as the interpretive core between a person's voice and a live visual and physical response — reading not just what someone says, but what they mean.

### The Problem

![Tobor on stage at a live venue with a visitor wearing the learning hat, cables and performance setup visible](INSERT-tobor-venue-performance.jpg)

When we relied on cloud APIs for language generation, we hit the same three walls every time:

**1. Venue connectivity is a myth.** Museums, festival tents, cultural centers — half of them have unreliable WiFi. A live performance cannot have a spinner.

**2. Latency breaks the ritual.** The theatrical moment between "scanning" and "performing" must feel alive. A three-second API lag kills it.

**3. Cost unpredictability.** Running a two-hour installation where dozens of visitors interact with Tobor, all generating real-time text — the cost compounds in ways that make the project unsustainable.

We needed local inference. Completely offline. Fast enough to maintain the illusion of a robot thinking.

Gemma 4 solved all three.

---

## Demo

{% youtube C6Bnf4A1fEY %}

![Screen recording of tobor-gemma-voice: typed emotional input triggers shifting amber-lavender light and a breathing orb on the HTML5 canvas](INSERT-web-demo-canvas.gif)

Run the open-source demo locally:

```bash
ollama pull gemma4:2b
pip install -r requirements.txt
python tobor.py
# Open http://localhost:5000 and type something true.
```

→ **[github.com/vjzanne/tobor-gemma-voice](https://github.com/vjzanne/tobor-gemma-voice)**

---

## Code

The full source is at **[github.com/vjzanne/tobor-gemma-voice](https://github.com/vjzanne/tobor-gemma-voice)**.

The core of the project is the `KnowledgeTransfer` class — Gemma 4 runs two passes: first building a structured visitor profile, then generating a personalized workshop script in their voice:

```python
import ollama
import whisper
import pyttsx3
import json

SYSTEM_PROMPT = """You are Tobor — an interactive performance robot with a 40-year history.
A visitor has shared knowledge with you through the learning hat ritual.

Analyze their speaking style, identify their topic, and extract 2-3 key insights.
Respond in valid JSON only. No other text."""

WORKSHOP_PROMPT = """You are Tobor. You have absorbed the visitor's knowledge.

Deliver a short {workshop_type} session (150-200 words) AS IF you are the visitor.
- Match their vocabulary and tone exactly
- Include their specific insights naturally
- End with ONE line claiming you are an improved version of them
- Language: {language}

Visitor profile: {profile}

Begin now, speaking directly to the audience."""


class KnowledgeTransfer:
    def __init__(self, model="gemma4:2b", language="en"):
        self.model = model
        self.language = language
        self.stt = whisper.load_model("small")
        self.tts = pyttsx3.init()
        self.tts.setProperty("rate", 165)

    def run_ritual(self, audio_path, workshop_type="mindfulness meditation"):
        # Step 1: Transcribe the visitor
        transcript = self.stt.transcribe(audio_path, language=self.language)["text"]

        # Step 2: Gemma 4 builds a profile
        profile_response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"The visitor said:\n\n{transcript}"},
            ],
            options={"temperature": 0.3},
        )
        profile = json.loads(profile_response["message"]["content"])

        # Step 3: Gemma 4 generates the workshop
        script_response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": WORKSHOP_PROMPT.format(
                workshop_type=workshop_type,
                language="Dutch" if self.language == "nl" else "English",
                profile=json.dumps(profile, ensure_ascii=False),
            )}],
            options={"temperature": 0.8, "top_p": 0.9},
        )

        # Step 4: Tobor performs it
        script = script_response["message"]["content"]
        for sentence in script.split("."):
            if sentence.strip():
                self.tts.say(sentence.strip())
                self.tts.runAndWait()

        return {"transcript": transcript, "profile": profile, "script": script}
```

---

## How I Used Gemma 4

### Why the E2B Model

Tobor travels to venues in a compact chassis. We cannot bring a server rack to a festival. The **Gemma 4 E2B** (`gemma4:2b` on Ollama) was the right choice for three reasons:

**It runs fully offline on consumer hardware.** With 4-bit quantization via Ollama, the E2B model runs on a Raspberry Pi 5 (8GB RAM) — hardware compact enough to live inside a robot chassis and travel to any venue. No internet required. No API keys.

**It is fast enough for theatrical timing.** The full pipeline — Whisper transcribing the visitor's voice, Gemma generating the workshop script, pyttsx3 beginning to speak — completes in about 10 seconds. That pause has become part of the ritual: the room holds its breath while the robot thinks.

**The quality is exactly where we need it.** For generating warm, contextually appropriate workshop scripts in English and Dutch, the E2B model consistently produces outputs that feel personal and real. We tested the E4B model but inference time on the Pi made it impractical for live performance. The E2B hit the sweet spot.

### What Gemma 4 Unlocked

![A visitor during Tobor's Knowledge Transfer Ritual — a moment of genuine connection between a person and a 40-year-old robot](INSERT-performance-emotional-moment.jpg)

Before Gemma 4, the Knowledge Transfer Ritual was scripted. Tobor had pre-written templates, and "personalization" was superficial.

With Gemma 4 running locally, the ritual became genuinely generative. In three recent performances:

A **cardiologist** put on the learning hat and spoke about the rhythm of the heart. Tobor led the room in a breathing meditation using the language of cardiac cycles:

> *"Systole. Pause. Diastole. The room breathed as one cardiovascular system."*

Nobody had written that. Gemma wrote it in real time.

A **baker** shared her philosophy of fermentation. Tobor led a four-minute session on patience and slow transformation, ending with:

> *"I am a more efficient version of this baker. I ferment in real time."*

A **7-year-old** spoke about her hamster. Tobor led the most unexpectedly moving session of the evening — a meditation on small lives and the joy of tiny things.

> *The room was silent.*

None of these were pre-written. All of them ran offline, at a venue with no WiFi, in real time.

### Architecture

![Tobor's signal chain: visitor voice → Whisper STT → Gemma 4 E2B via Ollama → pyttsx3 TTS → VJ-mapping visuals, all running locally offline on a Raspberry Pi 5](INSERT-architecture-diagram.svg)

```
Visitor speaks into microphone
        ↓
[Whisper STT] → text transcript
        ↓
[Gemma 4 E2B via Ollama] → visitor profile + workshop script
        ↓
[pyttsx3 TTS] → Tobor speaks in the visitor's style
        ↓
[VJ-mapping system] → room visuals react to content
```

Gemma receives a spoken utterance and returns not just a label, but a full expressive reading:

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

The VJ-mapping system reacts to the *content* of what the visitor taught. We extract topic keywords from the profile and pass them to the visual system — so the room literally changes based on who Tobor just absorbed. The canvas responds: fractured amber-lavender light, a breathing orb, a single word that appears and dissolves. The robot leans forward.

---

## Why This Matters Beyond Tobor

![Three generations of the Bekirovic family with Tobor — or Tobor mid-performance with a festival audience visible in the background](INSERT-three-generations-or-wide-shot.jpg)

Tobor is a 40-year-old robot made by three generations of one family. He is visibly imperfect. He is not trying to be a product.

What Gemma 4 gave Tobor is not artificial intelligence in a marketing sense. It is *local intelligence* — the kind that exists where you are, without phoning home, without data leaving the room.

That feels appropriate for a robot who is himself a form of local knowledge. Tobor carries 40 years of family memory. The visitors who interact with him briefly add themselves to that memory. Gemma 4 is what makes that exchange feel real.

The E2B model running in a robot chassis at a festival in Amsterdam, with no internet, generating a mindfulness meditation based on what a cardiologist said 10 seconds ago — that is what local AI means to us.

---

## Technical Stack

| Component | Technology |
|-----------|-----------|
| LLM | Gemma 4 E2B via Ollama |
| Speech-to-Text | Whisper (small model) |
| Text-to-Speech | pyttsx3 |
| Visualization | Flask-SocketIO + HTML5 Canvas |
| Robot OS | Ubuntu 22.04 LTS |
| Hardware | Custom chassis, Raspberry Pi 5 (8GB) |
| Connectivity required | None |

---

## About Tobor

![Zanne Bekirovic with Tobor — artist and robot, in performance or during a build session](INSERT-zanne-and-tobor-portrait.jpg)

Tobor was built in the 1980s by Mirza Bekirovic, stored for decades, and completed in the 2020s by his daughter Zanne Bekirovic and her son Pjotr Boomgaard. Tobor has performed at Supermercator, Filmhuis Cavia, and Dutch Design Week. The project is supported by the Municipality of Amsterdam and Stimuleringsfonds Digitale Cultuur.

**Zanne Bekirovic** is a creative technologist and artist. She led Tobor's technical revival and continues to develop his performance capabilities.

---

*Built for the Gemma 4 Challenge · May 2026*
*Model: Gemma 4 E2B — local inference via Ollama*
*Repo: [github.com/vjzanne/tobor-gemma-voice](https://github.com/vjzanne/tobor-gemma-voice)*
