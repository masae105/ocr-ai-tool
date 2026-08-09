# AI Development Log

## Lv4 Phase1：AI Provider基盤構築

### 目的

既存のLv3 OCR処理を壊さず、
将来的にOpenAI APIへ差し替え可能なAI解析層を追加する。

---

## Step 1：AI Provider設計

### Copilotへの指示

既存のLv3処理を壊さず、将来OpenAI APIへ差し替えられる構成で、
Lv4 Phase1の最小構成を提案してください。

条件：

- 既存OCR処理は変更しない
- OpenAI APIはまだ使用しない
- AI解析を別レイヤーとして追加する
- 後からProviderを差し替えられる構成にする

### 実装結果

- `src/ai_provider.py` を作成
- AI解析の共通インターフェースを定義

---

## Step 2：Mock AI Provider

### Copilotへの指示

OpenAI APIを使わず、
請求書のサンプルJSONを返すモック実装を作成してください。

### 実装結果

- `src/ai_mock_provider.py` を作成
- `MockAIProvider` を実装

---

## Step 3：AI Service

### Copilotへの指示

AI Providerを呼び出すサービス層を作成してください。

### 実装結果

- `src/ai_service.py` を作成
- Providerを利用してAI解析結果を返す構成にした

---

## Step 4：Provider設定

### Copilotへの指示

現在はmockを使用し、
将来OpenAIへ切り替えられる設定ファイルを作成してください。

### 実装結果

- `src/ai_config.py` を作成
- 現在のProviderを `mock` に設定

---

## Step 5：動作確認

### 実行内容

```python
from ai_service import AIService

service = AIService()

result = service.analyze("sample.png")

print(result)

### 実行内容

{'source': 'mock', 'file_name': 'sample.png', 'company_name': 'サンプル株式会社', 'invoice_date': '2026-08-09', 'total_amount': 125000, 'currency': 'JPY', 'items': [{'description': '開発費', 'amount': 100000}, {'description': '保守費', 'amount': 25000}]}

## Phase1 AI接続設計

### 接続位置
main.py の process_invoice 関数末尾

### 方針
既存のLv3処理完了後に AIService を呼び出す。

### 理由
- Lv3既存処理への影響を最小化
- 既存の戻り値構造を維持
- AI結果を ai_result として分離
- AI処理失敗時にもLv3結果を保持しやすい
- 将来的なAI APIへの差し替えを容易にする

### Phase1
AIServiceはモック実装とする。

### 将来
モック部分をLLM/API等の実AIサービスへ置き換え
る。

## Phase2 AI分析設計

### 目的
Lv3で構造化された請求書データをAIに渡し、
請求書の内容から異常・注意点を分析できる仕組みを構築する。

### AIに渡すデータ
Lv3の `data` 全体をAIServiceに渡す。

特定の項目だけを固定して渡すのではなく、
Lv3で生成されたデータをまとめてAIに渡すことで、
将来的な項目追加にも対応できる構成とする。

### AIの役割
Lv3で抽出・構造化されたデータをもとに、

- 金額の不整合
- 必須情報の欠落
- 不自然な明細
- その他の注意点

などを分析する。

### Lv3とLv4の役割分担

Lv3：
OCR結果から必要な情報を抽出し、構造化する。

Lv4：
構造化されたデータをAIが理解・分析し、
異常や注意点を判断する。

### データ構造

既存のLv3データは変更せず、
AIによる分析結果を `ai_result` として追加する。

```text
Lv3 data
    ↓
AIService
    ↓
AI分析結果
    ↓
data["ai_result"]

## Phase2 動作確認

### 確認内容

Lv3で解析された `data` 全体を `AIService` に渡し、
AI分析結果を `ai_result` として追加できることを確認した。

### 確認結果

- invoice1
  - 金額チェック：OK
  - AI判定：normal
  - デバッガーで確認

- invoice2
  - 金額チェック：NG
  - AI判定：warning
  - デバッガーで確認
  - スクリーンショット保存済み

### 確認事項

Lv3の既存処理を維持したまま、
Lv3の解析結果をPhase2のAI分析へ渡せることを確認した。

また、Lv3の金額チェック結果に応じて、
AIが `normal` / `warning` を返すことを確認した。

### スクリーンショット

invoice2のデバッガー画面を保存。

Lv3の「金額チェック：NG」と
Phase2の「AI status：warning」を確認できる。