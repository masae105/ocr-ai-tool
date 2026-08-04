import re


# 明細に混ざりやすいノイズキーワード
NOISE_WORDS = [
    "TEL",
    "FAX",
    "電話",
    "振込",
    "銀行",
    "口座",
    "担当",
    "〒",
    "http",
    "@",
    "請求書",
    "No"
]


# 電話番号パターン
PHONE_PATTERN = r"\d{2,4}-\d{2,4}-\d{4}"


def is_noise(item):
    """
    明細ノイズ判定
    """

    product_name = item.get("商品名", "")

    # OCRスペース除去
    product_name = product_name.replace(" ", "")

    # キーワードチェック
    for word in NOISE_WORDS:
        if word in product_name:
            return True

    # 電話番号チェック
    if re.search(PHONE_PATTERN, product_name):
        return True

    return False



def clean_details(details):
    """
    明細リストからノイズ除去
    """

    cleaned = []

    for item in details:

        if is_noise(item):
            continue

        cleaned.append(item)

    return cleaned

if __name__ == "__main__":

    test = [
        {"商品名": "商品A", "金額": 50000},
        {"商品名": "HDMIケーブル", "金額": 5000},
        {"商品名": "TEL 03-1234-5678", "金額": None},
        {"商品名": "○○銀行 振込先", "金額": None},
    ]

    print(clean_details(test))