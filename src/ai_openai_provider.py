import json

from openai import OpenAI

from ai_config import get_openai_api_key
from ai_provider import AIProvider

MODEL = "gpt-6-luna"

_RESULT_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["normal", "warning"]},
        "severity": {"type": "string", "enum": ["low", "medium", "high"]},
        "issues": {"type": "array", "items": {"type": "string"}},
        "recommendation": {"type": "string"},
        "correction_candidates": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "field": {"type": "string"},
                    "current_value": {"type": "string"},
                    "suggested_value": {"type": "string"},
                    "reason": {"type": "string"},
                    "confidence": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                    },
                },
                "required": [
                    "field",
                    "current_value",
                    "suggested_value",
                    "reason",
                    "confidence",
                ],
                "additionalProperties": False,
            },
        },
    },
    "required": [
        "status",
        "severity",
        "issues",
        "recommendation",
        "correction_candidates",
    ],
    "additionalProperties": False,
}

_DATA_FIELDS = (
    "書類タイプ",
    "金額チェック",
    "合計金額",
    "消費税",
    "請求日",
)


class OpenAIProvider(AIProvider):
    """OpenAI Responses APIで請求書の整合性を確認します。"""

    def analyze(self, data: dict) -> dict:
        api_key = get_openai_api_key()
        if not api_key:
            raise ValueError("OPENAI_API_KEY が設定されていません。")

        client = OpenAI(api_key=api_key)

        analysis_data = {
            field: data[field]
            for field in _DATA_FIELDS
            if field in data
        }
        if "明細" in data:
            analysis_data["明細"] = [
                {
                    field: item[field]
                    for field in ("商品名", "金額")
                    if field in item
                }
                for item in data["明細"]
            ]

        response = client.responses.create(
            model=MODEL,
            instructions=(
                "請求書の抽出データを整合性チェックしてください。"
                "OCR/Lv3から渡された情報だけを使い、"
                "元データから正しい値を確実に判断できない場合は補正候補を作らないでください。"
                "存在しない商品名や金額などを推測・創作しないでください。"
                "correction_candidatesは自動修正ではなく、人が確認するための候補です。"
                "明らかなOCRノイズや文字列混入は、正しい値を確実に判断できる場合に限り"
                "補正候補にしてかまいません。"
                "confidenceはlow、medium、highのいずれかにしてください。"
                "問題がなければcorrection_candidatesは空配列にしてください。"
                "金額を変更する候補は、渡された金額情報だけを根拠にしてください。"
                "suggested_valueが推測になる場合は候補を作らないでください。"
                "金額チェックが「NG」の場合は問題として扱ってください。"
                "問題がなければstatusはnormal、severityはlowにしてください。"
                "問題があればstatusはwarning、severityはmediumまたはhighにしてください。"
                "issuesとrecommendationは短い日本語にしてください。"
            ),
            input=json.dumps(analysis_data, ensure_ascii=False),
            text={
                "format": {
                    "type": "json_schema",
                    "name": "invoice_analysis",
                    "strict": True,
                    "schema": _RESULT_SCHEMA,
                }
            },
        )

        output_text = response.output_text
        if not isinstance(output_text, str) or not output_text.strip():
            raise ValueError("OpenAI APIから解析結果が返されませんでした。")

        result = json.loads(output_text)
        if not isinstance(result, dict):
            raise ValueError("OpenAI APIの解析結果がオブジェクトではありません。")

        required_fields = {
            "status",
            "severity",
            "issues",
            "recommendation",
            "correction_candidates",
        }
        if result.keys() != required_fields:
            raise ValueError("OpenAI APIの解析結果に必須項目がありません。")
        if result["status"] not in {"normal", "warning"}:
            raise ValueError("OpenAI APIのstatusが許容値ではありません。")
        if result["severity"] not in {"low", "medium", "high"}:
            raise ValueError("OpenAI APIのseverityが許容値ではありません。")
        if (
            result["status"] == "normal"
            and result["severity"] != "low"
        ) or (
            result["status"] == "warning"
            and result["severity"] not in {"medium", "high"}
        ):
            raise ValueError("OpenAI APIのstatusとseverityの組み合わせが不正です。")
        if not isinstance(result["issues"], list) or not all(
            isinstance(issue, str) for issue in result["issues"]
        ):
            raise ValueError("OpenAI APIのissuesが不正です。")
        if not isinstance(result["recommendation"], str):
            raise ValueError("OpenAI APIのrecommendationが不正です。")
        if not isinstance(result["correction_candidates"], list):
            raise ValueError("OpenAI APIのcorrection_candidatesが不正です。")
        candidate_fields = {
            "field",
            "current_value",
            "suggested_value",
            "reason",
            "confidence",
        }
        for candidate in result["correction_candidates"]:
            if not isinstance(candidate, dict) or candidate.keys() != candidate_fields:
                raise ValueError("OpenAI APIの補正候補の形式が不正です。")
            if not all(
                isinstance(candidate[field], str)
                for field in (
                    "field",
                    "current_value",
                    "suggested_value",
                    "reason",
                    "confidence",
                )
            ):
                raise ValueError("OpenAI APIの補正候補の項目が不正です。")
            if candidate["confidence"] not in {"low", "medium", "high"}:
                raise ValueError("OpenAI APIの補正候補のconfidenceが不正です。")

        return {
            "source": "openai",
            "status": result["status"],
            "severity": result["severity"],
            "issues": result["issues"],
            "recommendation": result["recommendation"],
            "correction_candidates": result["correction_candidates"],
        }
