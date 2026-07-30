import re


def clean_amount(value):

    if value is None:
        return None

    value = str(value)


      # 全角数字→半角数字
    value = value.translate(
        str.maketrans(
            "０１２３４５６７８９",
            "0123456789"
        )
    )

    replacements = {
        "O": "0",
        "o": "0",
        "l": "1",
        "I": "1",
        "①": "1",
        "②": "2",
        "③": "3",
        "④": "4",
        "⑤": "5",
        "⑥": "6",
        "⑦": "7",
        "⑧": "8",
        "⑨": "9",
    }


    for old, new in replacements.items():
        value = value.replace(old, new)


    # カンマ、円、空白削除
    value = re.sub(
        r"[¥￥円,\s]",
        "",
        value
    )


    # 数字だけ残す
    value = re.sub(
        r"[^0-9]",
        "",
        value
    )


    if value:
        return int(value)

    return None