# OCR AI Tool

## 📌 概要

PDFや画像から文字を自動認識（OCR）し、
請求書データを抽出・検証してExcelへ出力する自動化ツールです。

OCR文字補正、レイアウト判定、形式別データ抽出、
金額チェックまで実装し、異なる形式の請求書に対応しています。

---

## 🎯 開発目的

日常業務では、PDFや画像化された書類から必要な情報を手入力する作業が多く発生します。

そこで、

* PDF・画像の読み取り
* OCRによる文字抽出
* データ整理
* Excelへの自動入力

までをPythonで自動化するツールの開発に取り組みました。

---

## 🔄 処理フロー

請求書画像
 ↓
画像前処理
 ↓
OCR
 ↓
OCR文字補正
 ↓
特徴量抽出
 ↓
レイアウト判定(A/B/C)
 ↓
形式別データ抽出
 ↓
金額検証
 ↓
Excel出力


## 🚀 開発ロードマップ

### Lv1：OCR基本機能

* [x] PDF読み込み
* [x] 画像読み込み
* [x] OCRによる文字抽出
* [x] Excel自動出力

### Lv2：請求書OCR機能（完成）

* [x] 請求書読み取り
* [x] 項目別データ整理
* [x] Excelフォーマットへの自動入力
* [x] OCR文字補正
* [x] 金額チェック機能
* [x] OCR補正辞書による文字修正
* [x] 商品名補正辞書対応
* [x] 複数請求書処理
* [x] OCR金額異常候補検出

### Lv3：レイアウト解析・GUI対応（完成）

* [x] レイアウト判定基盤作成
* [x] OCR結果から特徴量抽出
* [x] レイアウトパターンJSON管理
* [x] スコアリングによるレイアウト判定
* [x] OCR座標情報を利用した領域分類
* [x] A/B/C形式ごとの抽出処理
* [x] 複数形式の請求書を自動処理
* [x] StreamlitによるGUI操作
* [x] 複数ファイル一括解析
* [x] Excelダウンロード機能

### Lv4：AIによる高度化

* [ ] AIによる書類レイアウト認識
* [ ] AIによる項目判定
* [ ] 自動データ振り分け
* [ ] LLMによるOCR補正

## ✅ 動作確認済み

異なる4種類の請求書フォーマットで動作確認しています。

| ファイル | 判定 | 内容 |
|---|---|---|
| invoice1.png | A | 基本形式請求書 |
| invoice2.png | B | 明細・税情報付き請求書 |
| invoice3.png | C | 別レイアウト請求書 |
| invoice4_test_company.png | C | 別会社フォーマット |

確認項目：

- 会社名抽出
- 請求日抽出
- 合計金額抽出
- 商品明細抽出
- Excel出力

## 📊 出力例

### Excel出力

請求書情報

|書類タイプ|会社名|請求番号|請求日|合計金額|金額チェック|
|-|-|-|-|-|-|
|請求書（Layout A）|株式会社ABC|-|2026年7月23日|55000|OK|
|請求書（Layout B）|株式会社XYZ|-|2026年7月28日|36500|OK|
|請求書（Layout C）|人サンプル商事株式会社|-|2026年7月30日|22500|NG|
|請求書（Layout C）|2サンプル商事株式会社|-|2026年7月30日|22500|NG|

※ 金額チェックNGはOCR誤認識や抽出差異を検出した結果であり、
データ検証機能によって確認対象として表示しています。

明細

|商品名|金額|
|-|-|
|商品A|50000|
|HDMIケーブル|5000|

---

## ▶️ 実行方法

### CLI実行
python src/main.py

GUI実行（Streamlit）
streamlit run app.py

# 🛠 使用技術

| 技術           | 用途                     |
| ------------ | ---------------------- |
| Python       | メイン開発言語               |
| Tesseract OCR | 文字認識エンジン             |
| pytesseract  | PythonからOCR処理を利用      |
| pandas       | データ処理                 |
| openpyxl     | Excel操作                |
| Pillow       | 画像処理                  |
| JSON         | OCR補正辞書・設定管理          |
| Streamlit    | GUI画面作成                |
| Git / GitHub | ソースコード管理              |

---

## 📂 ディレクトリ構成

```text
ocr-ai-tool
│
├── app.py
├── README.md
├── requirements.txt
├── LICENSE
│
├── data
│   ├── invoice_patterns.json
│   └── layout_patterns.json
│
├── docs
│   └── images
│       └── .gitkeep
│
├── output
│   └── .gitkeep
│
├── sample_data
│   ├── images
│   ├── invoices
│   └── pdf
│
└── src
    ├── main.py
    ├── loader.py
    ├── ocr.py
    ├── preprocess.py
    ├── cleaner.py
    ├── detail_cleaner.py
    │
    ├── extractor_a.py
    ├── extractor_b.py
    ├── extractor_c.py
    │
    ├── validator.py
    ├── amount_cleaner.py
    ├── excel.py
    │
    ├── layout_detector.py
    ├── feature_extractor.py
    ├── layout_analyzer.py
    ├── region_detector.py
    ├── region_fusion.py
    │
    └── ocr_dict
        ├── common.json
        ├── invoice.json
        ├── product.json
        ├── amount.json
        └── ocr_corrections.json
```

## 🔮 今後の課題・改善予定

### OCR精度向上

- 画像前処理の改善
- OCR認識精度の検証
- 補正辞書の拡充
- 商品名・金額補正ルールの強化


### Lv4：AIによる高度化

現在実装しているレイアウト判定基盤をさらに発展させ、
AIを活用した柔軟な書類解析を目指します。


#### AIによる書類レイアウト認識

- 請求書ごとの項目位置を自動認識
- 固定ルールに依存しないレイアウト解析
- 未知フォーマットへの対応


#### AIによる項目抽出

- 会社名・日付・金額・商品情報の自動判定
- 正規表現では対応が難しい書類への対応


#### AIによるOCR結果補正

- 文脈を考慮した誤認識修正
- 商品名・金額の妥当性判定
- 補正候補の自動提案


#### 書類分類機能

- 請求書・領収書・レシートの自動判別
- 書類種類に応じた処理分岐


## 📝 学習・開発目的

Pythonによる業務自動化スキル習得を目的として開発しています。

単なるOCR処理だけではなく、

* GitHubを利用した開発管理
* 可読性を意識したコード設計

にも取り組んでいます。
