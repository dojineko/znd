import sys
import subprocess
from pathlib import Path

def play_wav(wav_path: Path):
    if sys.platform == "darwin":
        subprocess.run(["afplay", str(wav_path)], check=True)
    elif sys.platform == "win32":
        try:
            import winsound
            winsound.PlaySound(str(wav_path), winsound.SND_FILENAME)
        except ImportError:
            subprocess.run(["powershell", "-c", f"(New-Object Media.SoundPlayer '{wav_path}').PlaySync()"], check=True)
    else:
        subprocess.run(["aplay", str(wav_path)], check=True)
