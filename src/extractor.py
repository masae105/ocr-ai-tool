import re


def extract_invoice_data(text):

    data = {}

        # 会社名
    company = re.search(
        r"(株式会社\s*\S+)",
        text
    )

    if company:
        data["会社名"] = company.group(1)

    # 明細
    data["明細"] = []

    # 請求番号
    invoice_no = re.search(
        r"請求.{0,2}[:：]?\s*(INV-\d+)",
        text
    )

    if invoice_no:
        data["請求番号"] = invoice_no.group(1)


    # 日付
    date = re.search(
        r"\d{4}\s*年?\s*\d{1,2}\s*月?\s*\d{1,2}\s*日?",
        text
    )

    if date:
        data["請求日"] = date.group()


    # 金額
    price = re.search(
        r"(合\s*計|総\s*額|請求\s*金額|合計金額).*?([0-9０-９,，.．]+)",
        text
    )

    if price:
        amount = price.group(2)

        # 全角数字を半角へ変換
        amount = amount.translate(
            str.maketrans("０１２３４５６７８９", "0123456789")
        )

        # カンマ・ピリオド除去
        amount = re.sub(r"[,.．，]", "", amount)

        data["合計金額"] = amount


     # 商品明細抽出
    lines = text.split("\n")

    for line in lines:

         # 合計金額は除外
        if "合計" in line:
            continue

         # OCR誤認識補正
        line = line.replace("S.", "5.")

        item = re.search(
            r"(.+?)\s+([0-9０-９,.]+)\s*[円日]",
            line
        )

        if item:

            item_name = item.group(1).replace("]", "").strip()
            
            amount = item.group(2)

            # 金額整形
            amount = amount.translate(
                str.maketrans("０１２３４５６７８９", "0123456789")
            )

            amount = re.sub(r"[,.．，]", "", amount)

            data["明細"].append({
                "商品名": item_name,
                "金額": amount
            })


    return data