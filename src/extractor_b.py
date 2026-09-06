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
    r"株式会社\s*[A-Za-zＡ-Ｚａ-ｚ0-9一-龥ぁ-んァ-ヶー・＆&.-]{1,20}",
    text
    )

    companies = [
        c.strip()
        for c in companies
        if "御中" not in c
    ]

    if companies:
        company_name = max(companies, key=len)

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

    item_names = []
    amount_values = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # ------------------------
        # 商品名候補
        # 例:
        # 1 ワイヤレスマウス
        # 2 。 キーボード
        # 3 24インチモニター
        # ------------------------
        item_match = re.match(
            r"^\s*\d+\s*[。.．]?\s*(.+)$",
            line
        )

        if item_match:
            item_name = item_match.group(1).strip()

            # 金額だけの文字列は商品名から除外
            # 例: \36,500- / ¥36,500 / 36,500-
            if not re.fullmatch(
                r"[¥\\]?[0-9０-９,.．]+-?",
                item_name
            ):
                item_names.append(item_name)
        # ------------------------
        # 金額行候補
        # 例:
        # \3,182 \3,182
        # ------------------------
        amounts = re.findall(
            r"[¥\\][0-9０-９][0-9０-９,.．]*",
            line
        )

        if len(amounts) >= 2:
            amount_values.append(
                clean_amount(amounts[-1])
            )


    # 商品名と金額を順番に対応付け
    for item_name, amount in zip(
        item_names,
        amount_values
    ):
        data["明細"].append(
            {
                "商品名": item_name,
                "金額": amount
            }
        )
    # ------------------------
    # 明細ノイズ除去
    # ------------------------

    data["明細"] = clean_details(
        data["明細"]
    )
    return data