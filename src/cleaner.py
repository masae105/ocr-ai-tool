import re


def clean_text(text):

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
        "商品きA": "商品A",
    }
    

    for old, new in replacements.items():
        text = text.replace(old, new)

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

    # 連続スペースを1つに変換
    text = re.sub(
        r"[ \u3000]+",
        " ",
        text    
    )


    # 前後の空白・改行削除
    text = text.strip()


    return text