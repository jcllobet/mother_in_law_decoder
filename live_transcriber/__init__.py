"""
Live Translator - Real-time transcription and translation.

Interactive UI with scroll mode for viewing conversation history.
"""

from .session import Session, SpeakerProfile
from .transcription import Transcriber, SAMPLE_RATE, NUM_CHANNELS, CHUNK_SIZE, list_audio_devices
from .ui import LiveTranscriptUI
from .languages import SONIOX_LANGUAGES, get_language_name, get_language_flag, get_all_language_codes

__all__ = [
    "Session",
    "SpeakerProfile",
    "Transcriber",
    "LiveTranscriptUI",
    "list_audio_devices",
    "SONIOX_LANGUAGES",
    "get_language_name",
    "get_language_flag",
    "get_all_language_codes",
    "SAMPLE_RATE",
    "NUM_CHANNELS",
    "CHUNK_SIZE",
]
