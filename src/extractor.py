import re


def extract_invoice_data(text):

    data = {}

    # 請求番号
    invoice_no = re.search(
        r"請求.{0,2}[:：]?\s*(INV-\d+)",
        text
    )

    if invoice_no:
        data["請求番号"] = invoice_no.group(1)


    # 日付
    date = re.search(
    r"\d{4}\s*年?\s*\d{1,2}\s*月?\s*\d{1,2}",
    text
    )

    if date:
        data["請求日"] = date.group()

    print("===== OCR全文 =====")
    print(text)

    # 金額
    price = re.search(
    r"(合\s*計|総\s*額|請求\s*金額).*?([0-9０-９,，]+)\s*円?",
    text
    )
    print("===== 金額検索結果 =====")
    print(price.groups() if price else "None")

    if price:
        data["合計金額"] = price.group(2)


    return data
