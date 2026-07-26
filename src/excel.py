import pandas as pd


def save_to_excel(results, output_path):
    """
    請求書データをExcelへ保存する
    """

    invoice_rows = []
    detail_rows = []

    for data in results:

        # 請求書情報
        invoice_rows.append({
            "会社名": data.get("会社名"),
            "請求番号": data.get("請求番号"),
            "請求日": data.get("請求日"),
            "合計金額": data.get("合計金額"),
            "金額チェック": data.get("金額チェック")
        })

        
         # 明細情報
        for item in data.get("明細", []):
            detail_rows.append({
                "請求番号": data.get("請求番号"),
                "商品名": item.get("商品名"),
                "金額": item.get("金額"),
            })

    invoice_df = pd.DataFrame(invoice_rows)

    detail_df = pd.DataFrame(detail_rows)


    with pd.ExcelWriter(output_path) as writer:

        invoice_df.to_excel(
            writer,
            sheet_name="請求書情報",
            index=False
        )

        detail_df.to_excel(
            writer,
            sheet_name="明細",
            index=False
        )

