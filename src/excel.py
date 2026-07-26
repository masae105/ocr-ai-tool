import pandas as pd


def save_to_excel(results, output_path):
    """
    請求書データを明細単位でExcelへ保存する
    """

    rows = []
    for data in results:

        for item in data.get("明細", []):

            rows.append({
                "会社名": data.get("会社名"),
                "請求番号": data.get("請求番号"),
                "請求日": data.get("請求日"),
                "商品名": item.get("商品名"),
                "金額": item.get("金額"),
                "金額チェック": data.get("金額チェック")
            })

    df = pd.DataFrame(rows)

    df.to_excel(
        output_path,
        index=False
    )

