import argparse
import sys
import tempfile
import os
from pathlib import Path
from .core import text_to_speech, get_default_paths, VoiceModelFile
from .audio import play_wav

def list_styles_cmd():
    paths = get_default_paths()
    models_dir = paths['models_dir']
    if not models_dir.exists():
        return

    all_styles = []
    for vvm_file in sorted(models_dir.glob("*.vvm")):
        if vvm_file.name.startswith("s"):
            continue
        try:
            with VoiceModelFile.open(str(vvm_file)) as model:
                for meta in model.metas:
                    for style in meta.styles:
                        all_styles.append((style.id, meta.name, style.name))
        except Exception:
            continue

    all_styles.sort(key=lambda x: (x[1], x[0]))
    current_char = None
    seen_styles = set()
    for style_id, char_name, style_name in all_styles:
        key = (char_name, style_name)
        if key in seen_styles:
            continue
        seen_styles.add(key)
        
        if char_name != current_char:
            print(f"\n{char_name}:")
            current_char = char_name
        print(f"  ID {style_id:5d}: {style_name}")

def find_style_id(speaker_name: str = None, style_name: str = None) -> int:
    paths = get_default_paths()
    models_dir = paths['models_dir']
    
    found_styles = []
    for vvm_file in models_dir.glob("*.vvm"):
        if vvm_file.name.startswith("s"):
            continue
        try:
            with VoiceModelFile.open(str(vvm_file)) as model:
                for meta in model.metas:
                    if speaker_name and meta.name != speaker_name:
                        continue
                    for style in meta.styles:
                        if not style_name or style.name == style_name:
                            found_styles.append((style.id, meta.name, style.name))
        except Exception:
            continue
    
    if not found_styles:
        print(f"Error: Style not found (speaker={speaker_name}, style={style_name})", file=sys.stderr)
        sys.exit(1)

    found_styles.sort(key=lambda x: x[0])
    return found_styles[0][0]

def main():
    parser = argparse.ArgumentParser(description='znd (VOICEVOX CLI)')
    parser.add_argument('text', nargs='?', help='Text to speak')
    parser.add_argument('--list', '-l', action='store_true', help='List styles')
    parser.add_argument('--speaker', '-p', help='Speaker name')
    parser.add_argument('--style', '-s', help='Style name')
    parser.add_argument('--sid', type=int, help='Style ID')
    parser.add_argument('--speed', type=float, default=1.2)
    parser.add_argument('--volume', type=float, default=2.0)
    parser.add_argument('--output', '-o', type=Path)
    parser.add_argument('--no-play', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')

    args = parser.parse_args()

    if args.list:
        list_styles_cmd()
        return

    if not args.text:
        parser.print_help()
        sys.exit(0)

    if args.sid is not None:
        style_id = args.sid
    else:
        style_id = find_style_id(args.speaker or "ずんだもん", args.style or "ノーマル")

    tmp_path = None
    try:
        output_path = args.output
        should_play = False
        if not output_path:
            fd, path = tempfile.mkstemp(suffix='.wav')
            os.close(fd)
            tmp_path = Path(path)
            output_path = tmp_path
            should_play = not args.no_play

        text_to_speech(args.text, output_path, style_id=style_id, speed_scale=args.speed, volume_scale=args.volume, verbose=args.verbose)

        if should_play:
            play_wav(output_path)

        if tmp_path and tmp_path.exists():
            tmp_path.unlink()
    except Exception as e:
        print(f"Error: {e}")
        if tmp_path and tmp_path.exists():
            tmp_path.unlink()
        sys.exit(1)

if __name__ == '__main__':
    main()
