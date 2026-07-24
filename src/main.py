from loader import load_file
from ocr import extract_text
from excel import save_to_excel
from pdf import pdf_to_images


def main():

    file_path = "sample_data/pdf/test.pdf"

    # ファイル読み込み
    path = load_file(file_path)

    # PDFを画像に変換
    images = pdf_to_images(path)

    results = []

    # 各ページをOCR
    for image in images:
        text = extract_text(image)
        results.append(text)


    # Excel保存
    output_path = "output/result.xlsx"

    save_to_excel(
        results,
        output_path

    )


if __name__ == "__main__":
    main()