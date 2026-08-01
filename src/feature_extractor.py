import re


def extract_features(text):
    """
    OCR結果から請求書特徴を抽出する

    Lv3 AIレイアウト判定用
    """

    features = {

        # 請求番号の有無
        "has_invoice_number": bool(
            re.search(
                r"(請求番号|Invoice|INV)",
                text,
                re.IGNORECASE
            )
        ),


        # 消費税の有無
        "has_tax": "消費税" in text,


        # 明細の有無
        # 商品名などの項目名
        # または金額が複数存在する場合
        "has_detail": (
            "商品名" in text
            or "数量" in text
            or "単価" in text
            or "明細" in text
            or len(
                re.findall(
                    r"\d{3,}",
                    text
                )
            ) >= 3
        ),


        # 数字の数
        "number_count": len(
            re.findall(
                r"\d+",
                text
            )
        ),


        # OCR文字数
        "text_length": len(text),

    }


    return features