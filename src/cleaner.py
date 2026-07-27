import re


def clean_text(text):
    """
    OCR結果の文字補正を行う

    処理内容:
    ・OCR誤認識修正
    ・数字表記統一
    ・請求書特有の誤認識修正
    ・不要な空白削除
    """

    replacements = {

        # 数字・文字補正
        "０": "0",
        "１": "1",
        "Ｏ": "O",
        "l": "1",

        # OCR誤認識補正
        "引crosoft": "Microsoft",
        "EdGe": "Edge",

        # 請求書OCR用補正
        "抹式会社": "株式会社",
        "請求恋": "請求書",
        "請求例殺": "請求金額",
        "合計全額": "合計金額",
        "昌": "円",
    }


    # 商品名補正
    product_replacements = {
        "HLSGLUM 1": "商品B",
        "HLSGLUM": "商品B",
        "商品きA": "商品A",
    }


    product_replacements = dict(
        sorted(
            product_replacements.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )
    )


    # 文字置換
    for old, new in replacements.items():
        text = text.replace(old, new)


    # 商品名補正
    for old, new in product_replacements.items():
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