import re
import json
import os

def load_dictionary():
    """
    OCR補正辞書(JSON)を読み込む
    """

    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "ocr_dictionary.json"
    )

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_text(text):
    """
    OCR結果の文字補正を行う

    処理内容:
    ・OCR誤認識修正
    ・数字表記統一
    ・請求書特有の誤認識修正
    ・商品名補正
    ・不要な空白削除
    """

    # JSON辞書読み込み
    replacements = load_dictionary()


    # 文字置換
    # 長い文字列を先に処理
    replacements = dict(
        sorted(
            replacements.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )
    )

    # 文字置換
    for old, new in replacements.items():
        text = text.replace(old, new)


    # 不要なダブルクォート削除
    text = text.replace('"', '')


    # OCR日付誤認識補正
    text = re.sub(
        r"(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})1\b",
        r"\1年\2月\3日",
        text
    )

    # 連続スペース削除
    text = re.sub(
        r"[ \u3000]+",
        " ",
        text
    )

    # 前後空白削除
    text = text.strip()


    return text