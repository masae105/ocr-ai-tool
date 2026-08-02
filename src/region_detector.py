"""
region_detector.py

OCR行情報を
header / detail / total / other
へ分類する

Lv3 Step3

layout_analyzer.py の
OCR行情報型に対応
"""


import re


# -------------------------
# キーワード
# -------------------------

HEADER_KEYWORDS = [
    "請求書",
    "請求番号",
    "請求No",
    "請求日",
    "発行日",
    "株式会社",
    "会社名",
    "御中",
    "〒",
]


DETAIL_KEYWORDS = [
    "商品",
    "商品名",
    "品名",
    "数量",
    "単価",
    "金額",
    "税抜",
    "明細",
    "内訳",
    "円",
]


TOTAL_KEYWORDS = [
    "合計",
    "合計金額",
    "合計全額",
    "請求金額",
    "ご請求金額",
    "小計",
    "消費税",
    "税込",
    "税額",
]


# -------------------------
# 商品明細判定
# -------------------------

def is_detail_line(text):
    """
    OCR文字列から
    商品明細らしさを判定

    例:
    1 ワイヤレスマウス 1 \3,182
    HDMIケーブル 1 5,000円
    """

    # 数字がある
    has_number = bool(
        re.search(
            r"\d",
            text
        )
    )


    # 金額っぽい文字がある
    has_money = bool(
        re.search(
            r"[¥\\￥]?\s*\d{1,3}[,\.]?\d+",
            text
        )
    )


    return has_number and has_money



# -------------------------
# 領域判定
# -------------------------

def detect_region(line):
    """
    OCR 1行から領域判定

    line:
    {
        "text": "...",
        "y": 123
    }
    """

    text = line["text"].strip()


    if not text:
        return "other"



    # 合計系を最優先
    for keyword in TOTAL_KEYWORDS:

        if keyword in text:

            return "total"



    # ヘッダー
    for keyword in HEADER_KEYWORDS:

        if keyword in text:

            return "header"



    # 明細キーワード
    for keyword in DETAIL_KEYWORDS:

        if keyword in text:

            return "detail"



    # 数字＋金額パターン
    # 商品名キーワードがなくても拾う
    if is_detail_line(text):

        return "detail"



    return "other"



# -------------------------
# OCR行を分類
# -------------------------

def split_regions(lines):
    """
    OCR行情報を
    header/detail/total/other
    に分類

    Parameters
    ----------
    lines:
        layout_analyzer.group_by_line()
        の戻り値

    """

    regions = {

        "header": [],
        "detail": [],
        "total": [],
        "other": []

    }



    for line in lines:

        region = detect_region(line)


        regions[region].append(
            {
                "text": line["text"],
                "y": line["y"],
                "region": region
            }
        )


    return regions