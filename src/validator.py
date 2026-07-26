def check_total_amount(data):
    """
    請求書合計金額と明細金額の合計を比較する

    Args:
        data(dict):
            請求書データ

    Returns:
        dict:
            金額チェック結果を追加したデータ
    """

    detail_total_amount = 0


    # 明細金額を合計
    for item in data.get("明細", []):

        detail_total_amount += int(
            item["金額"]
        )


    # 請求書合計金額
    invoice_total_amount = int(
        data.get("合計金額", 0)
    )


    # 金額比較
    if detail_total_amount == invoice_total_amount:
        data["金額チェック"] = "OK"

    else:
        data["金額チェック"] = "NG"


    return data