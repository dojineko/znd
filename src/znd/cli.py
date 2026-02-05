import argparse
import sys
import tempfile
import os
from pathlib import Path
from .core import text_to_speech, get_default_paths, VoiceModelFile
from .audio import play_wav

ZUNDAMON_STYLES = {
    'あまあま': 1,
    'ノーマル': 3,
    'normal': 3,
    'ツンツン': 7,
    'セクシー': 5,
    'ささやき': 22,
    'ヒソヒソ': 38,
    'ヘロヘロ': 75,
    'なみだめ': 76,
}

def list_styles_cmd():
    paths = get_default_paths()
    models_dir = paths['models_dir']
    if not models_dir.exists():
        print(f"Error: Model directory not found at {models_dir}")
        return

    print("=" * 70)
    print("Available Voice Styles")
    print("=" * 70)

    all_styles = []
    for vvm_file in sorted(models_dir.glob("*.vvm")):
        try:
            with VoiceModelFile.open(str(vvm_file)) as model:
                for meta in model.metas:
                    for style in meta.styles:
                        all_styles.append((style.id, meta.name, style.name))
        except Exception:
            continue

    all_styles.sort(key=lambda x: x[0])
    current_char = None
    for style_id, char_name, style_name in all_styles:
        if char_name != current_char:
            print(f"\n{char_name}:")
            current_char = char_name
        print(f"  ID {style_id:4d}: {style_name}")

def main():
    parser = argparse.ArgumentParser(description='znd (VOICEVOX CLI)')
    parser.add_argument('text', nargs='?', help='Text to speak')
    parser.add_argument('--list', '-l', action='store_true', help='List all available styles')
    parser.add_argument('--style', '-s', choices=list(ZUNDAMON_STYLES.keys()), default='ノーマル')
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

    style_id = ZUNDAMON_STYLES.get(args.style, 3)
    tmp_path = None
    try:
        if args.output:
            output_path = args.output
            should_play = False
        else:
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
