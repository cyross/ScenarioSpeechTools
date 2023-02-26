# ボイロ系動画作成支援システム

2023.1.27 Cyross Makoto

## 概要

VEGASでボイロ系動画を作成するための便利ツール集。
ツール全体で「ボイロ系動画作成支援システム(以降、本システム)」と称する

本システムは、以下の3つのツールで構成されている。

- CreateScenarioSpeechProject
  - セリフや字幕、出力音声ファイルを「プロジェクト」として管理している
  - そのためのフォルダやファイルを作成して、初期状態を構築する
- ScenarioSpeechSeparator
  - 一つのセリフファイルから、音声合成エンジン・声優別にファイルを振り分ける
  - 同時に、字幕用のファイルも生成する
- SpeechAudioFileRenamer
  - 動画編集ソフトの貼り付けのため、音声ファイルを一つのフォルダにまとめる
  - セリフの順番に音声ファイル名を連番に付け替える

## 動作環境

Python3が動く環境なら全て動く。
当方で開発している環境は以下のもの。

- Windows10 Pro x64
- Python 3.11
- PyYAML

- VOICEROID2
- VOICEPEAK
- CeVIO AI
- CeVIO CS7
- VOICEVOX

## ファイル構成

本システムの初期構成は以下の通り。

```text
. - config.example.yaml               # コンフィグファイルの雛形。config.yamlとして保存する
  - create_scenario_speech_project.py # CreateScenarioSpeechProject
  - scenario_speech_separator.py      # ScenarioSpeechSeparator
  - speech_audio_file_renamer.py      # SpeechAudioFileRenamer
  - utility.py                        # ユーティリティ関数群
  - LICENSE                           # ライセンスファイル(MITライセンス)
  - README.md                         # 本ファイル
  - .gitignore                        # git管理用
```

## 事前準備

本システムを使用する際は、事前に以下の準備をしておく。

### 1.Python3のインストール

既にインストールされている場合は不要

### 2.PyYAMLのインストール

既にインストールされている場合は不要

```bash
pip install pyyaml
```

### 3.config.yamlの準備

`config.example.yaml`を`config.yaml`にリネームしておく。
環境によって、`voice_engine`や`voice_actor`の設定を追加して保存する。

### 4.CeVIO CS・CeVIO AIのトーク設定

以下の設定になっていることを確認する。
（CeVIO CS・CeVIO AIのトーク設定は共通）

・テキストファイルの文字コード－読み込み - UTF-8(BOM自動)
・テキストファイルの文字コード－書き出し - UTF-8

CeVIO側で設定を変えたくない場合は、`config.yaml`の`output_file_encoding`の
設定を変更する。

- **例**

```yaml
"output_file_encoding":
  "VV": "utf-8"
  "VR": "shift_jis"
  "VP": "utf-8"
  "CC": "shift_jis" # 本の設定はutf-8
  "CA": "utf-8"
```

## VOICEPEAKでの注意事項

VOICEPEAKでは、テキストファイルをインポートする際に声優が固定される。
そのため、VOICEPEAK本体で声優を振り分ける必要がある。

## CreateScenarioSpeechProject

VEGASで使うボイロ系音声を管理するためのプロジェクトフォルダを生成

### CreateScenarioSpeechProjectの使い方

以下の順番で作成する。

#### 1.create_scenario_speech_project.pyの実行

```bash
python create_scenario_speech_project.py (プロジェクト名)
```

##### 1-2.作成されるファイル群

スクリプトを実行すると、以下の構成でフォルダやファイルが作られる。

- 実行例

前提として、以下の音声合成システムを用意しているとする。

- VOICEPEAK(VP)
- VOICEROID2(VR)
- VOICEVOX(VV)
- CeVIO AI(CA)
- CeVIO CS(CC)

```bash
python create_scenario_speech_project.py MyProject001
```

- フォルダ・ファイル群

```txt
./projects/MyProject001
  + output
    + VP
    + VR
    + VV
    + CA
    + CC
    + all
  + input
    + serifu.txt
```

- output : 音声合成エンジンによって生成された音声ファイルの保存場所
- output/(VP|VR|VV|CA|CC) : 各音声合成エンジン毎にディレクトリを分けて保存
- output/all : 最終的にVEGASのオーディオトラックに流し込む音声ファイルを保存する場所
  - speech_audio_file_renamer.pyで使う
- input : 入力ファイル用フォルダ
  - 音声合成エンジンや字幕として流し込むファイルが保存される
- serifu.txt : セリフファイル。ここにセリフを書き込む

## ScenarioSpeechSeparator

VEGASでのボイロ系動画を作成するために、複数エンジンで準備するセリフファイルを
各エンジン毎に所定の書式で振り分けて別々のファイルに保存する。
また、VEGASの字幕ファイルも同時に作成する。

### ScenarioSpeechSeparator使い方

以下の順番で処理する。

#### 1.セリフファイルの準備

`serifu.txt`を用意しておく（ファイル名はconfig.yamlで変更可能)

セリフの内容は以下。
行単位で書き込む。

`声優名,セリフ本体`

##### 1-1.セリフファイルの例

```txt
ずんだもん,ごきげんよう。おいらがずんだもんなのだ！
四国めたん(あまあま),ご機嫌麗しゅう。わらわは四国めたん。お見知りおきを。
琴葉茜,どないしたんや、こんなに甘い声出して！
```

#### 2.scenario_speech_separator.pyの実行

あとは、コマンドラインでスクリプトを実行すればOK！

```bash
python scenario_speech_separator.py (プロジェクト名)
```

コマンドライン引数の"./"は、serifu.txtが設置されているディレクトリ名を指す。

##### 2-2.ScenarioSpeechSeparatorで生成されるファイル

```bash
python scenario_speech_separator.py ./MyProject001
```

上記のコマンドで実行した際、以下のように生成される。

```txt
./projects/MyProject001
  + output
    + VP
    + VR
    + VV
    + CA
    + CC
    + all
  + input
    + serifu.txt
    + serifu_VP_(声優名).txt # 追加したファイル。声優名毎にファイルが作られる
    + serifu_VR.txt # 追加したファイル
    + serifu_VV.txt # 追加したファイル
    + serifu_CA.txt # 追加したファイル
    + serifu_CC.txt # 追加したファイル
    + jimaku.txt # 追加したファイル
```

- serifu_(エンジンの略称).txt : 各音声合成エンジン毎に振り分けたセリフファイル
  - serifu.txt中に対応する声優がある場合のみ作られる
  - VOICEPEAKでのセリフの流し込みは1声優のみのため、声優別にファイルが作られる
- jimaku.txt : 字幕流し込み用ファイル

## SpeechAudioFileRenamer

出力した音声ファイルをセリフの順番に連番を付けるためのスクリプト。

連番の順番は、serifu.txtで記載した順番で振られる。

対応する音声エンジンごとに出力された音声ファイルをallフォルダにコピーして、所定の番号に振り分ける。

### SpeechAudioFileRenamerの使い方

以下の順番で作成する。

#### 1.speech_audio_file_renamer.pyの実行

```bash
python speech_audio_file_renamer.py (プロジェクト名)
```

##### 1-2.SpeechAudioFileRenamerで作成されるファイル群

スクリプトを実行すると、以下の構成でフォルダやファイルが作られる。

- 実行例

```bash
python speech_audio_file_renamer.py ./MyProject001
```

- フォルダ・ファイル群

```txt
./projects/MyProject001
  + output
    + VP_(声優名)
      + 1.wav
      + 2.wav
      :
    + VR
      + 1.wav
      + 2.wav
      :
    + VV
      + 1.wav
      + 2.wav
      :
    + CA
      + 1.wav
      + 2.wav
      :
    + CC
      + 1.wav
      + 2.wav
      :
    + all
      + 0000000.wav # 生成されたファイル
      + 0000001.wav # 生成されたファイル
      + 0000002.wav # 生成されたファイル
      + 0000003.wav # 生成されたファイル
        :
  + input
    + serifu.txt
```

- output : 音声合成エンジンによって生成された音声ファイルの保存場所
- output/(VP_(声優名)|VR|VV|CA|CC) : 各音声合成エンジン毎にディレクトリを分けて保存
- output/all : 最終的にVEGASのオーディオトラックに流し込む音声ファイルを保存する場所
  - speech_audio_file_renamer.pyで使う
  - ファイル名は以下の書式で保存される
    - (セリフの連番).(音声ファイル拡張子)
  - 連番の桁数は`config.yaml`で変更可能
    - `"rename_digits": 7`
- input : 入力ファイル用フォルダ
  - 音声合成エンジンや字幕として流し込むファイルが保存される
- serifu.txt : セリフファイル。ここにセリフを書き込む

##### 1-3.SpeechAudioFileRenamerを使う際の注意事項

- jimaku.txtの行数と、保存しているオーディオファイルの数が同じである必要がある
- CeVIO CS/AIで使用するトラック数は一つのみに限定
  - 複数トラックで保存すると順番が狂うため
- serifu.txtでセリフを書く際は1行に1文を徹底する
  - VOICEROID2では、文節単位ではなく文単位で音声ファイルを作ってしまうため、jimaku.txtの行数と出力ファイル数の整合性が取れない
- **各音声合成エンジンでセリフを編集する際は、jimaku.txtの内容もそれに同期するように編集することが必須**
  - **セリフを追加するやセリフの順番を入れ替えたとき、場合によってはserifu.txtを編集して振り分け直したほうが好都合**
  - これを徹底しないと、順番が狂ったり、文節数とファイル数の不整合でエラーが起きる

### 免責事項

本システムは、MITライセンス下のもと、使用や再配布が可能です。

できれば、利用報告をいただけると当方が喜びます。

但し、本ドキュメントに登場する商品名は各ステークホルダーが権利を所持しております。

このスクリプトでは、各エンジン・声優の利用条件を遵守いたします。

本プロジェクト内で使用しているエンジン名・声優名は、データのキーワードとして使用しており、権利を侵害する目的で使用していないことを誓います。

そのため、**本プロジェクトを使用しての各エンジン・声優の許諾範囲を超える動画を作らないよう、強くお願い致します。**

各音声合成エンジン・各声優については、それぞれの許諾範囲をご確認ください。

### 各合成音声エンジンのライセンスリンク

#### AquesTalk

<https://www.a-quest.com/products/aquestalk.html>

#### ゆっくり音声（東方Project二次創作ガイドライン)

<https://touhou-project.news/guideline/>

#### A.I.VOICE

<https://aivoice.jp/>

#### VOICEROIDシリーズ

<https://www.ah-soft.com/voiceroid/>

#### VOICEPEAK

<https://www.ah-soft.com/voice/>

#### CeVIO CS

<https://cevio.jp/product/ccs/>

#### CeVIO AI

<https://cevio.jp/products_cevio_ai/>

#### VOICEVOX

<https://voicevox.hiroshiba.jp/>

## おまけ・VOICEROID2,CeVIOでのアドバイス

- VOICEROID2,CeVIOでは、音声ファイルを書き出す際に、セリフの両端に無音部分を作ることができる。
- 他のエンジンでは無音部分はつくらないため、それに合わせたほうが余計なことを考えずに済むので、設定で間隔を0にすることをお勧めする。
