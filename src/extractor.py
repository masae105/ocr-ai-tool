import re


def normalize_amount(value):
    """
    金額文字列を整形する

    処理内容:
    ・全角数字を半角へ変換
    ・カンマ、ピリオドを削除

    Args:
        value(str):
            OCRで取得した金額文字列

    Returns:
        str:
            整形後の金額
    """

    value = value.translate(
        str.maketrans(
            "０１２３４５６７８９",
            "0123456789"
        )
    )

    value = re.sub(r"[,.．，]", "", value)

    return value



def extract_invoice_data(text):
    """
    OCR結果から請求書データを抽出する

    抽出項目:
    ・会社名
    ・請求番号
    ・請求日
    ・合計金額
    ・商品明細

    Args:
        text(str):
            OCRで取得した請求書文字列

    Returns:
        dict:
            抽出した請求書データ
    """

    data = {}

    # ------------------------
    # 会社名抽出
    # ------------------------

    company = re.search(
        r"(株式会社\s*\S+)",
        text
    )

    if company:
        data["会社名"] = company.group(1)


    # ------------------------
    # 請求番号抽出
    # ------------------------

    invoice_no = re.search(
        r"請求.{0,2}[:：]?\s*(INV-\d+)",
        text
    )

    if invoice_no:
        data["請求番号"] = invoice_no.group(1)


    # ------------------------
    # 請求日抽出
    # ------------------------

    date = re.search(
        r"\d{4}\s*年?\s*\d{1,2}\s*月?\s*\d{1,2}\s*日?",
        text
    )

    if date:
        data["請求日"] = date.group()


    # ------------------------
    # 合計金額抽出
    # ------------------------

    total_amount = re.search(
        r"(合\s*計|総\s*額|請求\s*金額|合計金額).*?([0-9０-９,，.．]+)",
        text
    )

    if total_amount:

        amount = total_amount.group(2)

        data["合計金額"] = normalize_amount(amount)


    # ------------------------
    # 商品明細抽出
    # ------------------------

    data["明細"] = []

    lines = text.split("\n")

    for line in lines:

        # 合計金額行は明細対象外
        if "合計" in line:
            continue


        # OCR誤認識補正
        line = line.replace("S.", "5.")


        item = re.search(
            r"(.+?)\s+([0-9０-９,.]+)\s*[円日]",
            line
        )


        if item:

            item_name = (
                item.group(1)
                .replace("]", "")
                .strip()
            )

            # 商品名末尾の不要な数字削除
            # 例: 商品B 1 → 商品B
            item_name = re.sub(
                r"\s+\d+$",
                "",
                item_name
)

            amount = normalize_amount(
                item.group(2)
            )


            data["明細"].append(
                {
                    "商品名": item_name,
                    "金額": amount
                }
            )


    return data