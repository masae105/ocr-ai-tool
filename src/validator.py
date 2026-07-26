def check_total_amount(data):

    detail_total = 0

    for item in data.get("明細", []):
        detail_total += int(item["金額"])

    invoice_total = int(data.get("合計金額", 0))

    if detail_total == invoice_total:
        data["金額チェック"] = "OK"
    else:
        data["金額チェック"] = "NG"

    return data