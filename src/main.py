import os

from PIL import Image

from loader import load_file
from ocr import extract_text
from excel import save_to_excel
from preprocess import preprocess_image
from cleaner import clean_text
from extractor import extract_invoice_data
from validator import check_total_amount



IMAGE_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg"
)



def main():
    """
    請求書OCR処理のメイン処理

    処理内容:
    画像読み込み
    ↓
    OCR
    ↓
    文字補正
    ↓
    データ抽出
    ↓
    金額検証
    ↓
    Excel出力
    """

    folder_path = "sample_data/invoices"

    results = []


    files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(IMAGE_EXTENSIONS)
    ]


    for file in files:

        file_path = os.path.join(
            folder_path,
            file
        )

        # ファイル読み込み
        path = load_file(file_path)


        # 画像読み込み
        image = Image.open(path)


        # 画像前処理
        processed_image = preprocess_image(image)


        # デバッグ用画像保存
        processed_image.save("debug.png")


        # OCR実行
        text = extract_text(processed_image)

        print("===== OCR結果 =====")
        print(text)


        # OCR文字補正
        text = clean_text(text)

        print("===== OCR補正後 =====")
        print(text)


        # 請求書データ抽出
        data = extract_invoice_data(text)

        print("===== 抽出結果 =====")
        print(data)


        # 金額検証
        data = check_total_amount(data)

        print("===== 検証結果 =====")
        print(data)


        # 結果保存用リストへ追加
        results.append(data)



    # Excel出力
    output_path = "output/result.xlsx"


    save_to_excel(
        results,
        output_path
    )



if __name__ == "__main__":
    main()