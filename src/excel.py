import pandas as pd


def save_to_excel(results, output_path):
    """
    OCR結果をExcelへ保存する
    """

    df = pd.DataFrame({
        "OCR結果": results
    })

    df.to_excel(
        output_path,
        index=False
    )

