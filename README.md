# Mother-in-Law Decoder

Real-time transcription and translation for multilingual family conversations. 

Does your wife speak another language that you don't understand? Have you ever wondered what they're saying in the family dinner without wanting to stop the flow of conversation?

Note: _This does not currently decode subtle hints and other common in-laws language tactics._

## Quick Start

```bash
# Setup
python3.12 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then set SONIOX_API_KEY in .env

# Run
python main.py --session "xmas dinner"
```

## Usage

```bash
# Add context for better accuracy
python main.py --session "xmas dinner" --context "Family discussing vacation plans"
```

**Controls:** `v` to scroll history, `q` to quit and save.

## Selecting a Microphone

By default, the app auto-selects your MacBook's built-in microphone. To use a different device:

1. **List available devices:**
   ```bash
   python main.py --list-devices
   ```
   Output:
   ```
   Available audio input devices:
     [0] MacBook Pro Microphone (default)
     [1] USB Audio Device
     [2] AirPods Pro
   ```

2. **Run with your chosen device:**
   ```bash
   python main.py --session "xmas dinner" --device 1
   ```

### How debug audio issues:

If transcription shows "Waiting for speech..." but you're talking:

```bash
python debug_mic.py
```

This tests your microphone directly and shows a live audio level meter. Common fixes:
- **Permission denied:** System Settings → Privacy & Security → Microphone
- **Wrong device:** Try a different `--device` index
- **Muted mic:** Check system audio settings

## Output

Transcripts save to `output/<session>/` as JSON, TXT, and MP3. Resume anytime with the same session name or change it for a new session.

## Requirements

- Python 3.11+ (3.12 recommended)
- [Soniox API key](https://soniox.com)

## Supported Languages

🇸🇦 Arabic, 🪨 Basque, 🇧🇦 Bosnian, 🇧🇬 Bulgarian, 🐈 Catalan, 🇨🇳 Chinese, 🇭🇷 Croatian, 🇨🇿 Czech, 🇩🇰 Danish, 🇳🇱 Dutch, 🇺🇸 English, 🇪🇪 Estonian, 🇫🇮 Finnish, 🇫🇷 French, 🐟 Galician, 🇩🇪 German, 🇬🇷 Greek, 🇮🇳 Gujarati, 🇮🇱 Hebrew, 🇮🇳 Hindi, 🇭🇺 Hungarian, 🇮🇩 Indonesian, 🇮🇹 Italian, 🇯🇵 Japanese, 🇰🇷 Korean, 🇱🇻 Latvian, 🇱🇹 Lithuanian, 🇲🇰 Macedonian, 🇲🇾 Malay, 🇮🇳 Malayalam, 🇮🇳 Marathi, 🇳🇴 Norwegian, 🇮🇷 Persian, 🇵🇱 Polish, 🇵🇹 Portuguese, 🇮🇳 Punjabi, 🇷🇴 Romanian, 🇷🇺 Russian, 🇷🇸 Serbian, 🇸🇰 Slovak, 🇸🇮 Slovenian, 🇪🇸 Spanish, 🇸🇪 Swedish, 🇵🇭 Tagalog, 🇮🇳 Tamil, 🇮🇳 Telugu, 🇹🇭 Thai, 🇹🇷 Turkish, 🇺🇦 Ukrainian, 🇵🇰 Urdu, 🇻🇳 Vietnamese

---

MIT License
