def suggest_amount_fix(amount, invoice_total):
    """
    OCR誤認識した金額の補正候補を作成する

    Args:
        amount:
            OCR取得した金額
        invoice_total:
            請求書合計金額

    Returns:
        補正候補金額
    """

    amount = str(amount)
    invoice_total = int(invoice_total)

    candidates = []


    # 先頭1文字削除
    # 例: 55455 → 5455
    if len(amount) > 4:
        candidates.append(
            int(amount[1:])
        )


    # 末尾1文字削除
    # 例: 55455 → 5545
    if len(amount) > 4:
        candidates.append(
            int(amount[:-1])
        )


    # 候補の中から合計金額に近いものを選択

    best_candidate = None
    min_difference = float("inf")


    for candidate in candidates:

        difference = abs(
            candidate - invoice_total
        )

        if difference < min_difference:
            min_difference = difference
            best_candidate = candidate


    return best_candidate



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


    # 消費税
    tax = int(
        data.get("消費税", 0)
    )


    # 金額比較
    if (
        detail_total_amount == invoice_total_amount
        or
        detail_total_amount + tax == invoice_total_amount
    ):

        data["金額チェック"] = "OK"


    else:

        data["金額チェック"] = "NG"


        # ----------------------------
        # Lv2 金額補正候補検出
        # ----------------------------

        for item in data.get("明細", []):

            amount = int(
                item["金額"]
            )


            # 合計金額を超える明細は異常候補
            if amount > invoice_total_amount:


                item["金額補正候補"] = True


                item["補正候補金額"] = suggest_amount_fix(
                    amount,
                    invoice_total_amount
                )


    return data