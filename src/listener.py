"""
Voice Listener
==============
Captures microphone audio, detects speech via RMS silence detection,
and transcribes utterances using faster-whisper (local, CPU-friendly).
"""

import time
import wave
import numpy as np
from io import BytesIO
from typing import Callable, Optional

try:
    import sounddevice as sd
    import soundfile as sf
    _AUDIO_AVAILABLE = True
except ImportError:
    _AUDIO_AVAILABLE = False

try:
    from faster_whisper import WhisperModel
    _WHISPER_AVAILABLE = True
except ImportError:
    _WHISPER_AVAILABLE = False

SAMPLE_RATE = 16000
CHUNK_SIZE = 4000
MAX_RECORDING_SECONDS = 15
MAX_SILENT_FRAMES = 22       # ~2.2 s of silence ends the utterance
SILENCE_MULTIPLIER = 3.5     # threshold = background_rms * this


class VoiceListener:
    """
    Captures microphone audio and calls `on_utterance` with transcribed text.

    Requires: sounddevice, soundfile, faster-whisper
    """

    def __init__(
        self,
        language: str = "en",
        on_utterance: Optional[Callable[[str], None]] = None,
        whisper_model: str = "small",
    ):
        if not _AUDIO_AVAILABLE:
            raise RuntimeError(
                "Audio libraries missing. Install with:\n"
                "  pip install sounddevice soundfile"
            )
        if not _WHISPER_AVAILABLE:
            raise RuntimeError(
                "faster-whisper missing. Install with:\n"
                "  pip install faster-whisper"
            )

        self.language = language
        self.on_utterance = on_utterance
        self._silence_threshold: float = 300.0
        self._running = False

        print(f"  Loading Whisper ({whisper_model})...")
        self._model = WhisperModel(whisper_model, device="cpu", compute_type="int8")
        self._calibrate()

    def _calibrate(self, frames: int = 15):
        """Measure ambient noise floor to set silence threshold."""
        print("  Calibrating silence (2s)... ", end="", flush=True)
        rms_values = []
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16") as stream:
            for _ in range(frames):
                data, _ = stream.read(CHUNK_SIZE)
                rms_values.append(_rms(data))
                time.sleep(0.1)
        self._silence_threshold = max(np.median(rms_values) * SILENCE_MULTIPLIER, 100)
        print(f"threshold={self._silence_threshold:.0f}")

    def run(self):
        """Main loop: wait for speech, transcribe, fire callback. Blocks until Ctrl+C."""
        self._running = True
        print("  Listening for voice... (Ctrl+C to stop)\n")
        try:
            while self._running:
                text = self._capture_utterance()
                if text and self.on_utterance:
                    self.on_utterance(text)
        except KeyboardInterrupt:
            print("\n\n  Tobor goes quiet.\n")

    def _capture_utterance(self) -> Optional[str]:
        """Record until silence ends the utterance; return transcribed text."""
        audio_buf = BytesIO()
        detected = False
        silent_frames = 0
        max_frames = int(MAX_RECORDING_SECONDS * SAMPLE_RATE / CHUNK_SIZE)

        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16") as stream, \
             wave.open(audio_buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)

            for _ in range(max_frames):
                data, _ = stream.read(CHUNK_SIZE)
                loud = _rms(data) > self._silence_threshold

                if loud:
                    detected = True
                    silent_frames = 0
                    wf.writeframes(data.tobytes())
                elif detected:
                    silent_frames += 1
                    wf.writeframes(data.tobytes())
                    if silent_frames >= MAX_SILENT_FRAMES:
                        break

        if not detected:
            return None

        audio_buf.seek(0)
        audio, _ = sf.read(audio_buf, dtype="float32")
        audio = np.clip(audio, -1.0, 1.0)

        segments, _ = self._model.transcribe(
            audio, language=self.language, temperature=0.0, beam_size=1
        )
        text = " ".join(s.text for s in segments).strip()
        return text or None


def _rms(data: np.ndarray) -> float:
    return float(np.sqrt(np.mean(data.astype(np.float64) ** 2)))
