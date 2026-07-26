import os

from loader import load_file
from ocr import extract_text
from excel import save_to_excel
from preprocess import preprocess_image
from cleaner import clean_text
from extractor import extract_invoice_data
from validator import check_total_amount

from PIL import Image


def main():

    folder_path = "sample_data/invoices"

    results = []


    # フォルダ内の請求書を取得
    files = os.listdir(folder_path)


    for file in files:

        file_path = os.path.join(
            folder_path,
            file
        )


        # ファイル読み込み
        path = load_file(file_path)


        # 画像読み込み
        image = Image.open(path)


        # 前処理
        processed_image = preprocess_image(image)


        # デバッグ保存
        processed_image.save("debug.png")


        # OCR
        text = extract_text(processed_image)

        print("===== OCR結果 =====")
        print(text)


        # OCR文字補正
        text = clean_text(text)

        print("===== OCR全文 =====")
        print(text)


        # 項目抽出
        data = extract_invoice_data(text)

        print("===== 抽出結果 =====")
        print(data)


        # 金額チェック
        data = check_total_amount(data)

        print("===== 検証結果 =====")
        print(data)


        results.append(data)



    # Excel保存
    output_path = "output/result.xlsx"


    save_to_excel(
        results,
        output_path
    )


if __name__ == "__main__":
    main()