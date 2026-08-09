import os

from PIL import Image

from cleaner import clean_text
from excel import save_to_excel
from extractor_a import extract_a
from extractor_b import extract_b
from extractor_c import extract_c
from loader import load_file
from ocr import extract_text, extract_data
from preprocess import preprocess_image
from validator import check_total_amount

from layout_detector import detect_layout
from feature_extractor import extract_features
from layout_analyzer import group_by_line, detect_regions
from region_detector import split_regions
from region_fusion import merge_regions
from ai_service import AIService



IMAGE_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg"
)


def process_invoice(file_path):
    """
    1枚の請求書画像を解析する処理

    流れ:
    画像読み込み
    ↓
    OCR
    ↓
    文字補正
    ↓
    レイアウト解析
    ↓
    データ抽出
    ↓
    金額検証
    """

    path = load_file(file_path)

    image = Image.open(path)

    # 画像前処理
    processed_image = preprocess_image(image)


    # OCR取得
    text = extract_text(processed_image)


    # 座標付きOCR
    ocr_data = extract_data(processed_image)

    lines = group_by_line(
        ocr_data
    )


    # Lv3 レイアウト領域解析
    coordinate_regions = detect_regions(lines)

    keyword_regions = split_regions(lines)

    regions = merge_regions(
        coordinate_regions,
        keyword_regions
    )


    # OCR文字補正
    text = clean_text(text)


    # 特徴量取得
    features = extract_features(text)


    # レイアウト判定
    layout = detect_layout(
        text,
        features
    )

    # レイアウト別抽出
    if layout == "A":
        data = extract_a(text)

    elif layout == "B":
        data = extract_b(text)

    elif layout == "C":
        data = extract_c(text)

    else:
        data = {}

    # 金額チェック
    data = check_total_amount(data)

    # 書類タイプ追加
    data["書類タイプ"] = f"請求書（Layout {layout}）"

    # Phase2 AI解析
    ai_service = AIService()
    ai_result = ai_service.analyze(data)

    # AI結果を追加
    data["ai_result"] = ai_result

    return data


  

def main():

    folder_path = "sample_data/invoices"

    results = []


    files = [
        f
        for f in os.listdir(folder_path)
        if f.lower().endswith(IMAGE_EXTENSIONS)
    ]


    for file in files:

        file_path = os.path.join(
            folder_path,
            file
        )


        print("解析中:", file)


        data = process_invoice(
            file_path
        )
        
        results.append(data)


        print(
            f"完了: {file}"
        )


    # Excel出力

    output_path = "output/result.xlsx"


    save_to_excel(
        results,
        output_path
    )


    print()
    print("====================")
    print("OCR処理完了")
    print(f"Excel: {output_path}")
    print("====================")



if __name__ == "__main__":
    main()