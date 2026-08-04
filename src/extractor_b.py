import re
import json
import os

from amount_cleaner import clean_amount
from detail_cleaner import clean_details


def load_invoice_patterns():

    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "invoice_patterns.json"
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)



def extract_b(text):

    data = {}

    patterns = load_invoice_patterns()


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

        data["会社名"] = (
            company_name
            .replace(" ", "")
            .replace("　", "")
        )


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
            rf"{keyword}.*?([0-9０-９,，.．]+)",
            text
        )

        if total_amount:

            data["合計金額"] = clean_amount(
                total_amount.group(1)
            )

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
        # 商品名 数量 単価 金額
        # ------------------------

        detail = re.search(
            r"^\s*\d+\s+(.+?)\s+\d+\s+[\¥\\]?[0-9０-９,.．]+\s+[\¥\\]?[0-9０-９,.．]+",
            line
        )


        if detail:

            item_name = detail.group(1).strip()


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
    # 明細ノイズ除去
    # ------------------------

    data["明細"] = clean_details(
        data["明細"]
    )


    return data