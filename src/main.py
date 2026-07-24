from loader import load_file
from ocr import extract_text
from excel import save_to_excel


def main():

    file_path = "sample_data/images/test2.png"

    # ファイル読み込み
    path = load_file(file_path)

    # OCR実行
    text = extract_text(path)

    print("===== OCR結果 =====")
    print(text)

    # Excel保存
    save_to_excel(
        text,
        "output/result.xlsx"
    )

    print("処理が完了しました！")


if __name__ == "__main__":
    main()