import re
import json
import os

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

    company = re.search(
        r"(株式会社\s*\S+)",
        text
    )

    if company:
        data["会社名"] = company.group(1)


    # ------------------------
    # 請求番号抽出
    # ------------------------

    for keyword in patterns["請求番号"]:

        invoice_no = re.search(
            rf"{keyword}.*?([A-Za-z0-9]+-\d+)",
            text
        )

        if invoice_no:
            data["請求番号"] = invoice_no.group(1)
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
            rf"{keyword}.*?([0-9０-９,，.．]+)",
            text
        )

        if total_amount:

            amount = total_amount.group(1)

            data["合計金額"] = normalize_amount(amount)

            break


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