import pandas as pd


def save_to_excel(text, output_path):
    """
    OCR結果をExcelへ保存する
    """

    df = pd.DataFrame({
        "OCR結果": [text]
    })

    df.to_excel(
        output_path,
        index=False
    )


if __name__ == "__main__":

    text = "OCRテスト結果"

    save_to_excel(
        text,
        "output/result.xlsx"
    )

    print("Excel保存完了")