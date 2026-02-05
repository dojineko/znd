# ZND (VOICEVOX CLI)

コマンドラインから日本語テキストを音声に変換するPythonツール。ずんだもんを始めとしたVOICEVOXの各種キャラクターを利用できます。

## セットアップ手順

### 1. 前提条件

- [Python 3.8+](https://www.python.org/)
- [git](https://git-scm.com/)

### 2. リポジトリの取得

```bash
git clone https://github.com/dojineko/znd.git
cd znd
```

### 3. 日本語辞書（Open JTalk）のダウンロード

[Open JTalk の配布ページ](https://jaist.dl.sourceforge.net/project/open-jtalk/Dictionary/open_jtalk_dic-1.11/open_jtalk_dic_utf_8-1.11.tar.gz) から辞書をダウンロードし、リポジトリ直下に `open_jtalk_dic_utf_8-1.11` ディレクトリとして展開してください。

### 4. 実行に必要なファイルのダウンロード (Downloader)

VOICEVOX Core の動作に必要な依存ライブラリや音声モデルをダウンロードします。
[公式の最新リリース](https://github.com/VOICEVOX/voicevox_core/releases/latest/)から、環境に合った Downloader を取得して実行してください。

**Windows の場合:**
`download-windows-x64.exe` をダウンロードし、以下のコマンドを実行します。

```powershell
.\download-windows-x64.exe
```

**macOS (Apple Silicon) の場合:**
`download-osx-arm64` をダウンロードし、実行権限を付与して実行します。

```bash
chmod +x download-osx-arm64
./download-osx-arm64
```

実行後、リポジトリ直下に `voicevox_core` ディレクトリが作成され、その中に必要なファイルがダウンロードされます。

### 5. Python ライブラリのインストール

環境に合わせた wheel ファイルを[公式リリース](https://github.com/VOICEVOX/voicevox_core/releases/tag/0.16.3)からダウンロードしてインストールしてください。

- **Windows (x64)**: `voicevox_core-0.16.3-cp310-abi3-win_amd64.whl`
- **macOS (Apple Silicon)**: `voicevox_core-0.16.3-cp310-abi3-macosx_11_0_arm64.whl`

```bash
# インストール例
pip install https://github.com/VOICEVOX/voicevox_core/releases/download/[バージョン]/voicevox_core-[バージョン]+[デバイス]-cp310-abi3-[OS・アーキテクチャ].whl
```

### 6. znd コマンドのインストール

プロジェクトを編集モードでインストールします。

```bash
pip install -e .
```

## 使い方

### スタイル一覧を表示する

```bash
znd --list
# または
znd -l
```

### テキストを読み上げる

デフォルトで「ずんだもん（ノーマル）」が読み上げます。

```bash
# 基本的な使い方
znd "こんにちは、ずんだもんなのだ"

# スタイルを指定
znd "こんにちは" --style ツンツン
znd "こんにちは" -s ヒソヒソ
znd "こんにちは" -s なみだめ

# 速度を調整
znd "こんにちは" --speed 1.5

# 音量を調整（デフォルト: 2.0）
znd "こんにちは" --volume 3.0

# ファイルに保存
znd "こんにちは" --output hello.wav
```

**利用可能なスタイル（ずんだもん）:**
`あまあま`, `ノーマル`, `ツンツン`, `セクシー`, `ささやき`, `ヒソヒソ`, `ヘロヘロ`, `なみだめ`
