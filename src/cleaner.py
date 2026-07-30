import json
import os
import re


DICTIONARY_FILES = (
    "common.json",
    "invoice.json",
    "product.json",
    "amount.json"
)


DICTIONARY_DIR = os.path.join(
    os.path.dirname(__file__),
    "ocr_dict"
)


def load_dictionary():
    """
    OCR補正用JSON辞書を読み込む

    common:
        一般的なOCR誤認識

    invoice:
        請求書特有の誤認識

    product:
        商品名補正

    amount:
        金額補正
    """

    replacements = {}

    for file_name in DICTIONARY_FILES:

        path = os.path.join(
            DICTIONARY_DIR,
            file_name
        )

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        replacements.update(data)

    return replacements

def clean_text(text):
    """
    OCR結果を整形する

    処理内容:
    ・OCR誤認識補正
    ・請求書用語補正
    ・商品名補正
    ・金額補正
    ・不要文字削除
    ・空白整理
    """

    # JSON辞書読み込み
    replacements = load_dictionary()

    # 長い文字列を先に処理
    replacements = dict(
        sorted(
            replacements.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )
    )

    # 文字補正
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
    return text.strip()