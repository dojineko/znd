import multiprocessing
from pathlib import Path
from typing import Optional
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile
import sys

_synthesizer_cache = None
_onnxruntime_cache = None

def get_default_paths():
    """OSに応じたデフォルトのパス設定を取得"""
    package_dir = Path(__file__).parent
    project_root = package_dir.parent.parent

    if sys.platform == "win32":
        onnx_name = "voicevox_onnxruntime.dll"
    elif sys.platform == "darwin":
        onnx_name = "libvoicevox_onnxruntime.1.17.3.dylib"
    else:
        onnx_name = "libvoicevox_onnxruntime.so"

    return {
        'dict_dir': project_root / 'open_jtalk_dic_utf_8-1.11',
        'models_dir': project_root / 'voicevox_core' / 'models' / 'vvms',
        'onnxruntime': project_root / 'voicevox_core' / 'onnxruntime' / 'lib' / onnx_name
    }

def find_model_for_style(models_dir: Path, style_id: int) -> Optional[Path]:
    """指定されたスタイルIDを持つモデルファイルを探す"""
    for vvm_file in models_dir.glob("*.vvm"):
        try:
            with VoiceModelFile.open(str(vvm_file)) as model:
                for meta in model.metas:
                    for style in meta.styles:
                        if style.id == style_id:
                            return vvm_file
        except Exception:
            continue
    return None

def initialize_synthesizer(
    dict_dir: Optional[Path] = None,
    onnxruntime_path: Optional[Path] = None
) -> Synthesizer:
    global _synthesizer_cache, _onnxruntime_cache

    if _synthesizer_cache is not None:
        return _synthesizer_cache

    paths = get_default_paths()
    dict_dir = dict_dir or paths['dict_dir']
    onnxruntime_path = onnxruntime_path or paths['onnxruntime']

    if not dict_dir.exists():
        raise FileNotFoundError(f"OpenJTalk辞書が見つかりません: {dict_dir}")

    if _onnxruntime_cache is None:
        if onnxruntime_path.exists():
            _onnxruntime_cache = Onnxruntime.load_once(filename=str(onnxruntime_path))
        else:
            _onnxruntime_cache = Onnxruntime.load_once()

    _synthesizer_cache = Synthesizer(
        _onnxruntime_cache,
        OpenJtalk(dict_dir),
        acceleration_mode="AUTO",
        cpu_num_threads=max(multiprocessing.cpu_count(), 2)
    )

    return _synthesizer_cache

def text_to_speech(
    text: str,
    output_path: Path,
    style_id: int = 3,
    models_dir: Optional[Path] = None,
    dict_dir: Optional[Path] = None,
    onnxruntime_path: Optional[Path] = None,
    verbose: bool = False,
    speed_scale: float = 1.2,
    volume_scale: float = 2.0
) -> None:
    paths = get_default_paths()
    models_dir = models_dir or paths['models_dir']

    if not models_dir.exists():
        raise FileNotFoundError(f"モデルディレクトリが見つかりません: {models_dir}")

    if verbose:
        print(f"スタイルID {style_id} のモデルを検索中...", file=sys.stderr)

    model_file = find_model_for_style(models_dir, style_id)
    if not model_file:
        raise ValueError(f"スタイルID {style_id} のモデルが見つかりません")

    synthesizer = initialize_synthesizer(dict_dir, onnxruntime_path)

    with VoiceModelFile.open(str(model_file)) as model:
        try:
            synthesizer.load_voice_model(model)
        except Exception:
            pass

    audio_query = synthesizer.create_audio_query(text, style_id)
    audio_query.speed_scale = speed_scale
    audio_query.volume_scale = volume_scale
    wav = synthesizer.synthesis(audio_query, style_id)

    Path(output_path).write_bytes(wav)
