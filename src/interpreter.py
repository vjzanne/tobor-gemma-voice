"""
Gemma 4 Resonance Engine
=========================
The interpretive core of Tobor. Sends voice transcripts to Gemma 4
and receives structured relational states — not labels, but readings.
All inference runs locally via Ollama — no internet required.
"""

import json
import re
from typing import Optional

try:
    import ollama
    _OLLAMA_AVAILABLE = True
except ImportError:
    _OLLAMA_AVAILABLE = False

SYSTEM_PROMPT = """You are the empathic core of Tobor — a therapy-art robot that witnesses human stories.

Listen to what is said. Beneath the words, find:
- The relational undercurrent
- What it costs the speaker to say this
- What they need to be seen

Respond ONLY with a valid JSON object. No explanation. No text before or after the JSON.

{
  "emotion": "<one of: tender|vulnerable|conflicted|warm|hesitant|longing|tense|fierce|absent|playful>",
  "intensity": <float 0.0–1.0, how strongly this emotion radiates>,
  "energy": <float 0.0–1.0, where 0.0=still/collapsed and 1.0=vibrating/kinetic>,
  "resonance": "<one single word that names what is really being said>",
  "visual_mode": "<one of: fragmented_glow|pulse_soft|spiral_inward|scatter_bright|still_deep|wave_gentle|tremor_bright|collapse_dark|bloom_warm|flicker_void>",
  "robot_state": "<one of: attentive|leaning_in|withdrawn|open|still|reaching>"
}"""

FALLBACK_STATE = {
    "emotion": "absent",
    "intensity": 0.3,
    "energy": 0.2,
    "resonance": "listening",
    "visual_mode": "still_deep",
    "robot_state": "attentive",
}

_VALID_EMOTIONS = {
    "tender", "vulnerable", "conflicted", "warm", "hesitant",
    "longing", "tense", "fierce", "absent", "playful"
}
_VALID_VISUAL_MODES = {
    "fragmented_glow", "pulse_soft", "spiral_inward", "scatter_bright",
    "still_deep", "wave_gentle", "tremor_bright", "collapse_dark",
    "bloom_warm", "flicker_void"
}
_VALID_ROBOT_STATES = {
    "attentive", "leaning_in", "withdrawn", "open", "still", "reaching"
}

# Keyword fallback when Ollama is unavailable
_FALLBACK_KEYWORDS = {
    "tender":     ["gentle", "soft", "delicate", "care", "careful"],
    "vulnerable": ["afraid", "scared", "exposed", "hurt", "broken", "ashamed"],
    "conflicted": ["but", "however", "yet", "torn", "confused", "both", "and yet"],
    "warm":       ["love", "heart", "together", "home", "safe", "held", "belong"],
    "hesitant":   ["maybe", "perhaps", "unsure", "don't know", "not sure", "wonder"],
    "longing":    ["miss", "want", "wish", "far", "gone", "remember", "used to"],
    "tense":      ["angry", "tight", "pressure", "stress", "must", "have to", "can't"],
    "fierce":     ["never", "always", "fight", "strong", "power", "refuse", "won't"],
    "playful":    ["laugh", "funny", "joke", "fun", "play", "silly", "smile"],
}


class GemmaInterpreter:
    """Reads expressive resonance from text using Gemma 4 via Ollama."""

    def __init__(self, model: str = "gemma4:2b"):
        self.model = model
        self._last_state = dict(FALLBACK_STATE)

    def check_connection(self) -> bool:
        """Verify Ollama is running and the model is available."""
        if not _OLLAMA_AVAILABLE:
            return False
        try:
            models = ollama.list()
            available = [m["name"] for m in models.get("models", [])]
            base = self.model.split(":")[0]
            return any(base in m for m in available)
        except Exception:
            return False

    def interpret(self, text: str) -> dict:
        """
        Send text to Gemma 4 and receive a validated relational state dict.
        Falls back gracefully if Ollama is unavailable or returns malformed output.
        """
        if not _OLLAMA_AVAILABLE or not text.strip():
            return self._keyword_fallback(text)

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text.strip()},
                ],
                options={"temperature": 0.4, "top_p": 0.9},
            )
            raw = response["message"]["content"]
            state = self._parse(raw)
            self._last_state = state
            return state

        except Exception as e:
            print(f"\n  [warn] Gemma error: {e}")
            return dict(self._last_state)

    def _parse(self, raw: str) -> dict:
        """Extract and validate JSON from Gemma's response."""
        # Strip markdown code fences
        raw = re.sub(r"```(?:json)?\s*", "", raw).strip().rstrip("`")

        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            return dict(FALLBACK_STATE)

        try:
            data = json.loads(match.group())
        except json.JSONDecodeError:
            return dict(FALLBACK_STATE)

        emotion = data.get("emotion", "absent")
        visual_mode = data.get("visual_mode", "still_deep")
        robot_state = data.get("robot_state", "attentive")

        return {
            "emotion": emotion if emotion in _VALID_EMOTIONS else "absent",
            "intensity": max(0.0, min(1.0, float(data.get("intensity", 0.5)))),
            "energy": max(0.0, min(1.0, float(data.get("energy", 0.3)))),
            "resonance": str(data.get("resonance", "silence"))[:32],
            "visual_mode": visual_mode if visual_mode in _VALID_VISUAL_MODES else "still_deep",
            "robot_state": robot_state if robot_state in _VALID_ROBOT_STATES else "attentive",
        }

    def _keyword_fallback(self, text: str) -> dict:
        """Simple keyword-based fallback when Ollama is unavailable."""
        text_lower = text.lower()
        for emotion, keywords in _FALLBACK_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return {**FALLBACK_STATE, "emotion": emotion, "resonance": emotion}
        return dict(FALLBACK_STATE)
