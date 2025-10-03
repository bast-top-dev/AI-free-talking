# AI エージェント - 電話営業ボット

日本語での音声対話が可能なAIエージェントアプリケーションです。Tkinterを使用したGUIと、音声認識・音声合成機能を搭載しています。

## プロジェクト構造

```
AI-free-talking/
├── ai_agent/                    # メインパッケージ
│   ├── __init__.py
│   ├── config/                  # 設定管理
│   │   ├── __init__.py
│   │   └── settings.py         # アプリケーション設定
│   ├── ui/                     # UIコンポーネント
│   │   ├── __init__.py
│   │   └── main_window.py      # メインウィンドウ
│   ├── speech/                 # 音声処理
│   │   ├── __init__.py
│   │   ├── tts_engine.py       # 音声合成エンジン
│   │   └── speech_recognizer.py # 音声認識エンジン
│   └── conversation/           # 会話管理
│       ├── __init__.py
│       └── conversation_manager.py
├── main.py                     # メインアプリケーション
├── run.py                      # 簡単起動スクリプト
├── setup.py                    # セットアップスクリプト
├── requirements.txt            # 依存関係
├── ai_agent_old.py            # 旧版（参考用）
└── Readme.md                  # このファイル
```

## 機能

- **音声対話**: マイクからの音声認識とスピーカーへの音声出力
- **日本語対応**: 日本語の音声認識と日本語女性ボイスでの音声合成
- **会話履歴**: リアルタイムでの会話内容表示
- **音量制御**: スライダーでの音量調整
- **声の高さ可視化**: 音声出力時の視覚的フィードバック
- **テキスト入力**: 手動でのテキスト送信機能
- **会話管理**: 開始・停止・初期化・ログクリア機能
- **モジュラー設計**: 保守性と拡張性を考慮した構造

## 必要な環境

- Python 3.7以上
- Windows/macOS/Linux対応

## 🚀 クイックスタート

### 最も簡単な方法 (Windows)
```bash
# ダブルクリックで実行
start_ai_agent.bat
```

### 最も簡単な方法 (Linux/macOS)
```bash
# 実行権限を付与して実行
chmod +x start_ai_agent.sh
./start_ai_agent.sh
```

### 手動実行
```bash
# 1. 依存関係をインストール
pip install -r requirements.txt

# 2. アプリケーションを実行
python main.py
# または
python run.py
```

## 📦 本番環境への展開

詳細な展開方法については [DEPLOYMENT.md](DEPLOYMENT.md) を参照してください。

### スタンドアロン実行ファイル作成 (Windows)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "AI_Agent" main.py
```

### Docker コンテナ
```bash
docker build -t ai-agent .
docker run -it --device /dev/snd ai-agent
```

## アーキテクチャの特徴

### モジュラー設計
- **分離された責任**: 各モジュールが明確な責任を持つ
- **保守性**: 個別の機能を独立して修正・拡張可能
- **テスタビリティ**: 各コンポーネントを単独でテスト可能
- **再利用性**: 他のプロジェクトでコンポーネントを再利用可能

### 主要コンポーネント
- **MainWindow**: UI表示とユーザーインタラクション管理
- **TTSEngine**: 音声合成とボイス制御
- **SpeechRecognizer**: 音声認識とマイク制御
- **ConversationManager**: 会話フローとレスポンス生成
- **Settings**: 設定管理とコンフィグレーション

## 使用方法

1. **開始ボタン**: 会話を開始します
2. **停止ボタン**: 会話を停止します
3. **テキスト送信**: 手動でテキストを送信できます
4. **ログクリア**: 会話履歴をクリアします
5. **会話初期化**: 会話を最初からやり直します
6. **音量制御**: スライダーで音量を調整できます

## 注意事項

- マイクとスピーカーが必要です
- インターネット接続が必要です（Google Speech Recognition使用）
- 初回実行時に音声エンジンの初期化に時間がかかる場合があります

## トラブルシューティング

### PyAudio インストールエラーの場合
**Windows (最も一般的な問題):**
```bash
pip install pipwin
pipwin install pyaudio
```
詳細なWindowsセットアップガイド: [WINDOWS_SETUP.md](WINDOWS_SETUP.md)

macOSの場合:
```bash
brew install portaudio
pip install pyaudio
```

Linux (Ubuntu/Debian)の場合:
```bash
sudo apt-get install python3-pyaudio
pip install pyaudio
```

### 音声認識が動作しない場合
- マイクが正しく接続されているか確認
- マイクのアクセス許可が与えられているか確認
- インターネット接続を確認

### 日本語音声が再生されない場合
- システムに日本語音声エンジンがインストールされているか確認
- 他の言語でも動作確認
