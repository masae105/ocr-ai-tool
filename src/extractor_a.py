import re
import json
import os
from amount_cleaner import clean_amount

def load_invoice_patterns():
    """
    請求書抽出パターン(JSON)を読み込む
    """

    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "invoice_patterns.json"
    )

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_a(text):

    data = {}

    patterns = load_invoice_patterns()
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

    # ------------------------
    # 会社名抽出
    # ------------------------

    companies = re.findall(
    r"(?:株式会社\s*[^\n〒()（）]{1,20}|[^\n〒()（）]{1,20}株式会社)",
    text
    )

    companies = [
        c.strip()
        for c in companies
        if "御中" not in c
    ]

    if companies:

        company_name = max(
            companies,
            key=len
        )

        company_name = (
            company_name
            .replace(" ", "")
            .replace("　", "")
        )

        data["会社名"] = company_name

    # ------------------------
    # 請求番号抽出 強化 Lv2
    # ------------------------

    invoice_patterns = [

        # 請求番号: INV-001
        r"(?:請求番号|請求書番号|請求恋)\s*[:：]?\s*([A-Za-z0-9]+-?\d+)",

        # Invoice No: INV001
        r"(?:Invoice.*?No|Invoice\s*Number)\s*[:：]?\s*([A-Za-z0-9]+-?\d+)"
    ]


    for pattern in invoice_patterns:

        invoice_no = re.search(
            pattern,
            text,
            re.IGNORECASE
        )


        if invoice_no:

            invoice_number = invoice_no.group(1)


            # INV001 → INV-001へ統一
            if "-" not in invoice_number:

                invoice_number = re.sub(
                    r"([A-Za-z]+)(\d+)",
                    r"\1-\2",
                    invoice_number
                )


            data["請求番号"] = invoice_number

            break

    # ------------------------
    # 請求日抽出
    # ------------------------

    for keyword in patterns["請求日"]:

        date = re.search(
        rf"{keyword}.*?(\d{{4}}[\s年/-]*\d{{1,2}}[\s月/-]*\d{{1,2}}日?)",
        text
    )

        if date:
            data["請求日"] = (
                date.group(1)
                .replace(" ", "")
            )
            break


    # ------------------------
    # 合計金額抽出
    # ------------------------

    for keyword in patterns["合計金額"]:

        total_amount = re.search(
            rf"{keyword}[\s\S]*?[\\¥￥]?\s*([0-9０-９,，.．]+)",
            text
        )

        if total_amount:

            amount = total_amount.group(1)

            data["合計金額"] = clean_amount(amount)

            break
    # ------------------------
    # 消費税抽出
    # ------------------------

    for line in text.split("\n"):

        if "消費税" not in line:
            continue

        amounts = re.findall(
            r"[0-9０-９,，.．]+",
            line
        )

        if amounts:

            data["消費税"] = clean_amount(
                amounts[-1]
            )

            break


    # ------------------------
    # 商品明細抽出
    # ------------------------

    data["明細"] = []

    lines = text.split("\n")

    for line in lines:

        if "合計" in line:
            continue

        # OCR誤認識補正
        line = line.replace("S.", "5.")
        line = line.replace("「", "")
        line = line.replace("]", "")
        line = line.replace("ぎ", "")
        line = line.replace("、", ",")
        line = line.replace("|", "")

        # ------------------------
        # 新形式
        # 1 商品名 数量 単価 金額
        # ------------------------

        detail = re.search(
            r"^\s*\d+\s+(.+?)\s+\d+\s+[\¥\\]?[0-9０-９,.．]+\s+[\¥\\]?[0-9０-９,.．]+",
            line
        )


        if detail:

            item_name = detail.group(1).strip()


            # 最後の金額を取得
            amounts = re.findall(
                r"[\¥\\]?[0-9０-９,.．]+",
                line
            )


            if amounts:

                amount = clean_amount(
                    amounts[-1]
                )


                data["明細"].append(
                    {
                        "商品名": item_name,
                        "金額": amount
                    }
                )

                continue



        # ------------------------
        # 旧形式
        # 商品名 金額
        # ------------------------

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


            item_name = re.sub(
                r"\s+\d+$",
                "",
                item_name
            )


            amount = clean_amount(
                item.group(2)
            )


            data["明細"].append(
                {
                    "商品名": item_name,
                    "金額": amount
                }
            )

    return data        