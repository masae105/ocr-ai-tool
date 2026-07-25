from loader import load_file
from ocr import extract_text
from excel import save_to_excel
from pdf import pdf_to_images
from preprocess import preprocess_image
from cleaner import clean_text
from extractor import extract_invoice_data
from PIL import Image


def main():

    file_path = "sample_data/pdf/invoice.png"

    # ファイル読み込み
    path = load_file(file_path)

    # 画像の場合
    images = [Image.open(path)]

    results = []

    for image in images:

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


        results.append(text)


    # Excel保存
    output_path = "output/result.xlsx"

    save_to_excel(
        results,
        output_path

    )


if __name__ == "__main__":
    main()