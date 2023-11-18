# ボイロ系動画作成支援システム

2023.11.18 Cyross Makoto

## 概要

VEGAS でボイロ系動画を作成するための便利ツール集。
ツール全体で「ボイロ系動画作成支援システム(以降、本システム)」と称する

本システムは、以下の 3 つのツールで構成されている。

- BuildProject
  - セリフや字幕、出力音声ファイルを「プロジェクト」として管理している
  - そのためのフォルダやファイルを作成して、初期状態を構築する
- SeparateScenario
  - 一つのセリフファイルから、音声合成エンジン・声優別にファイルを振り分ける
  - 同時に、字幕用のファイルも生成する
- CopyAndRename
  - 動画編集ソフトの貼り付けのため、音声ファイルを一つのフォルダにまとめる
  - セリフの順番に音声ファイル名を連番に付け替える

## 動作環境

Python3 が動く環境なら全て動く。
当方で開発している環境は以下のもの。

- Windows10 Pro x64
- Python 3.11
- PyYAML

- A.I.VOICE
- VOICEROID2
- VOICEPEAK
- CeVIO AI
- CeVIO CS7
- VOICEVOX,VOICEVOX Nemo
- Voisona Talk

## サポートしている音声合成エンジン

本システムでサポートしている音声合成エンジンは以下

(注意)但し AquesTalk は動作未確認

- A.I.VOICE(AIV)
- AquesTalk(AQ)
- CeVIO AI(CA)
- CeVIO CS(CC)
- VOICEPEAK(VP)
- VOICEROID2(VR)
- VOICEVOX,VOICEVOX Nemo(VV)
- Voisona Talk(VT)

## 音声合成エンジンを使用していないもの

また、音声合成エンジンを使用していない場合も、以下のパターンでサポートしている

- その他(OTHER)
  - サポートしていない音声合成エンジンを使用した場合に使う
  - 生声や生音声のファイルを使用する場合に使う
- 音声なし(NONE)
  - 単に字幕として表示させたいときなど、音声を伴わないものとして使う

## ファイル構成

本システムの初期構成は以下の通り。

```text
. - config.yaml          # コンフィグファイル
  - actor.yaml           # actor情報
  - engine.yaml          # engine情報
  - build_project.py     # BuildProject
  - separate_scenario.py # SeparateScenario
  - copy_and_rename.py   # CopyAndRename
  - scenario             # pythonのモジュール
  - LICENSE                           # ライセンスファイル(MITライセンス)
  - README.md                         # 本ファイル
  - .gitignore                        # git管理用
```

## 事前準備

本システムを使用する際は、事前に以下の準備をしておく。

### 1.Python3 のインストール

既にインストールされている場合は不要

### 2.PyYAML のインストール

既にインストールされている場合は不要

```bash
pip install pyyaml
```

### 3.config.yaml の準備

`config.example.yaml`を`config.yaml`にリネームしておく。
環境によって、`voice_engine`や`voice_actor`の設定を追加して保存する。

### 4.CeVIO CS・CeVIO AI のトーク設定

以下の設定になっていることを確認する。
（CeVIO CS・CeVIO AI のトーク設定は共通）

・テキストファイルの文字コード－読み込み - UTF-8(BOM 自動)
・テキストファイルの文字コード－書き出し - UTF-8

CeVIO 側で設定を変えたくない場合は、`config.yaml`の`output_file_encoding`の
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

## VOICEPEAK での注意事項

VOICEPEAK では、テキストファイルをインポートする際に声優が固定される。
そのため、VOICEPEAK 本体で声優を振り分ける必要がある。

## BuildProject

VEGAS で使うボイロ系音声を管理するためのプロジェクトフォルダを生成

### BuildProject の使い方

以下の順番で作成する。

#### 1.build_project.py の実行

```bash
python build_project.py (プロジェクト名)
```

##### 1-2.作成されるファイル群

スクリプトを実行すると、以下の構成でフォルダやファイルが作られる。

- 実行例

```bash
python build_project.py MyProject001
```

- フォルダ・ファイル群

```txt
./projects/MyProject001
  + output
    + AIV
    + all
    + AQ
    + CA
    + CC
    + NONE
    + OTHER
    + VP_(声優名)
    + VR
    + VV
  + input
    + serifu.txt
```

- output : 音声合成エンジンによって生成された音声ファイルの保存場所
- output/(AIV|AQ|CA|CC|NONE|OTHER|VP\_(声優名)|VR|VV) : 各音声合成エンジン毎にディレクトリを分けて保存
- output/all : 最終的に VEGAS のオーディオトラックに流し込む音声ファイルを保存する場所
  - copy_and_rename.py で使う
- input : 入力ファイル用フォルダ
  - 音声合成エンジンや字幕として流し込むファイルが保存される
- serifu.txt : セリフファイル。ここにセリフを書き込む

## SeparateScenario

VEGAS でのボイロ系動画を作成するために、複数エンジンで準備するセリフファイルを
各エンジン毎に所定の書式で振り分けて別々のファイルに保存する。
また、VEGAS の字幕ファイルも同時に作成する。

### SeparateScenario 使い方

以下の順番で処理する。

#### 1.セリフファイルの準備

`serifu.txt`を用意しておく（ファイル名は config.yaml で変更可能)

##### 1-1.セリフファイルの書式

セリフの基本的な書式は以下。

```csv
声優名,セリフ本体
```

1 行中に行単位で書き込む。
複数行の内容を 1 行に書いてしまうと、CopyAndRename でエラーを出すため注意！

声優名を `[なし]` もしくは `ナレーター` と指定すると、VOICE ENGINE を `NONE` として処理する。
その際、セリフの先頭にそのセリフを表示させる時間を指定できる。

```csv
声優名,[(数値)]セリフ本体
```

カッコ内の数値は**ミリ秒単位**で指定できる。1 秒のときは `1000` と記述する。

省略した際は、各自(VegasHelper)の標準設定に従う。

##### 1-2.セリフファイル記述時の注意

`config.yaml` で指定していない声優名を書き込むと、エラーを出さずに VOICE ENGINE を "OTHER" として処理するため、**書き間違えに注意！**

##### 1-3.セリフファイルの例

```csv
ずんだもん,ごきげんよう。おいらがずんだもんなのだ！
四国めたん(あまあま),ご機嫌麗しゅう。わらわは四国めたん。お見知りおきを。
琴葉茜,どないしたんや、こんなに甘い声出して！
[VV]ずんだもん,VOICEVOXで喋らせるときはここなのだ！
[VP]ずんだもん,VOICEPEAKでも明示できるのだ！
[なし],ナレーションできますか？
ナレーター,[1000]ナレーションできます
どこかの誰か,発声練習します
```

#### 2.separate_scenario.py の実行

あとは、コマンドラインでスクリプトを実行すれば OK！

```bash
python separate_scenario.py (プロジェクト名)
```

コマンドライン引数の"./"は、serifu.txt が設置されているディレクトリ名を指す。

##### 2-1.SeparateScenario で生成されるファイル

```bash
python separate_scenario.py MyProject001
```

上記のコマンドで実行した際、以下のファイルが追加される。

```txt
./projects/MyProject001
  + output
    (変更なし)
  + input
    + serifu_(Voice Engine).txt
    + jimaku.txt
    + jimaku_raw.txt
```

各ファイルの説明は以下。

- serifu\_(Voice Engine).txt : 各音声合成エンジン毎に振り分けたセリフファイル
  - serifu.txt 中に対応する声優がある場合のみ作られる
  - VOICEPEAK でのセリフの流し込みは 1 声優のみのため、声優別にファイルが作られる
    - "VP\_(声優名)"
- jimaku.txt : 字幕流し込み用ファイル(流し込めるように編集済み)
- jimaku*raw.txt : serifu*(Voice Engine).txt の内容をそのまま一つにしたファイル

##### 2-2.SeparateScenario を使う際の注意事項

- Voice Engine が OTHER の音声ファイルは、すべて output/OTHER フォルダに保存する
- output/OTHER フォルダに保存する際、ファイル名は CopyAndRename で想定通りにソートできるように名付ける必要がある
  - ファイル名の先頭をゼロ埋めの連番にしておくと、想定通りの順番で Rename がなされる
  - 例：00001-～.wav

## CopyAndRename

出力した音声ファイルをセリフの順番に連番を付けるためのスクリプト。

連番の順番は、serifu.txt で記載した順番で振られる。

対応する音声エンジンごとに出力された音声ファイルを all フォルダにコピーして、所定の番号に振り分ける。

### CopyAndRename の使い方

以下の順番で作成する。

#### 1.copy_and_rename.py の実行

```bash
python copy_and_rename.py (プロジェクト名)
```

##### 1-2.CopyAndRename で作成されるファイル群

スクリプトを実行すると、以下の構成でフォルダやファイルが作られる。

- 実行例

```bash
python copy_and_rename.py MyProject001
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
- output/(VP\_(声優名)|VR|VV|CA|CC) : 各音声合成エンジン毎にディレクトリを分けて保存
- output/all : 最終的に VEGAS のオーディオトラックに流し込む音声ファイルを保存する場所
  - copy_and_rename.py で使う
  - ファイル名は以下の書式で保存される
    - (セリフの連番).(音声ファイル拡張子)
  - 連番の桁数は`config.yaml`で変更可能
    - `"rename_digits": 7`
- input : 入力ファイル用フォルダ
  - 音声合成エンジンや字幕として流し込むファイルが保存される
- serifu.txt : セリフファイル。ここにセリフを書き込む

##### 1-3.CopyAndRename を使う際の注意事項

- jimaku.txt の行数と、保存しているオーディオファイルの数が同じである必要がある
- CeVIO CS/AI で使用するトラック数は一つのみに限定
  - 複数トラックで保存すると順番が狂うため
- serifu.txt でセリフを書く際は 1 行に 1 文を徹底する
  - VOICEROID2 では、文節単位ではなく文単位で音声ファイルを作ってしまうため、jimaku.txt の行数と出力ファイル数の整合性が取れない
- **各音声合成エンジンでセリフを編集する際は、jimaku.txt の内容もそれに同期するように編集することが必須**
  - **セリフを追加するやセリフの順番を入れ替えたとき、場合によっては serifu.txt を編集して振り分け直したほうが好都合**
  - これを徹底しないと、順番が狂ったり、文節数とファイル数の不整合でエラーが起きる

### 免責事項

本システムは、MIT ライセンス下のもと、使用や再配布が可能です。

できれば、利用報告をいただけると当方が喜びます。

但し、本ドキュメントに登場する商品名は各ステークホルダーが権利を所持しております。

このスクリプトでは、各エンジン・声優の利用条件を遵守いたします。

本プロジェクト内で使用しているエンジン名・声優名は、データのキーワードとして使用しており、権利を侵害する目的で使用していないことを誓います。

そのため、**本プロジェクトを使用しての各エンジン・声優の許諾範囲を超える動画を作らないよう、強くお願い致します。**

各音声合成エンジン・各声優については、それぞれの許諾範囲をご確認ください。

### 各合成音声エンジンのライセンスリンク

#### AquesTalk

<https://www.a-quest.com/products/aquestalk.html>

#### ゆっくり音声（東方 Project 二次創作ガイドライン)

<https://touhou-project.news/guideline/>

#### A.I.VOICE

<https://aivoice.jp/>

#### VOICEROID シリーズ

<https://www.ah-soft.com/voiceroid/>

#### VOICEPEAK

<https://www.ah-soft.com/voice/>

#### CeVIO CS

<https://cevio.jp/product/ccs/>

#### CeVIO AI

<https://cevio.jp/products_cevio_ai/>

#### VOICEVOX

<https://voicevox.hiroshiba.jp/>

#### VOICEVOX Nemo

<https://voicevox.hiroshiba.jp/nemo/>

#### Voisona Talk

<https://voisona.com/talk/>

## 謝辞

ゆっくり音声名については、以下のサイトを参考させて頂いております。

ありがとうございます。

- [ユウイナちゃんねるのブログ 東方ゆっくりボイス一覧](https://ameblo.jp/staffoz/entry-12701709291.html)
- [nicotalk & キャラ素材配布所 きつねゆっくり](http://www.nicotalk.com/charasozai_kt.html)
- [nicotalk & キャラ素材配布所 新きつねゆっくり](http://www.nicotalk.com/charasozai_sky.html)
- [東方 MMD まとめ 東方 Project のキャラクター一覧と読み方](https://imimatome.com/touhoummd/kyara/638/)

## おまけ・VOICEROID2,CeVIO でのアドバイス

- VOICEROID2,CeVIO では、音声ファイルを書き出す際に、セリフの両端に無音部分を作ることができる。
- 他のエンジンでは無音部分はつくらないため、それに合わせたほうが余計なことを考えずに済むので、設定で間隔を 0 にすることをお勧めする。
