import pytesseract
from pytesseract import Output


# Tesseractの場所を指定
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)



def extract_text(image):
    """
    画像から文字を抽出する
    """

    text = pytesseract.image_to_string(
        image,
        lang="jpn"
    )

    return text



def extract_data(image):
    """
    OCR結果 + 座標情報を取得する

    Lv3 レイアウト認識用
    """

    data = pytesseract.image_to_data(
        image,
        lang="jpn",
        output_type=Output.DICT
    )


    results = []


    for i in range(len(data["text"])):

        text = data["text"][i].strip()


        # 空文字除外
        if text == "":
            continue


        results.append(
            {
                "text": text,
                "x": data["left"][i],
                "y": data["top"][i],
                "width": data["width"][i],
                "height": data["height"][i],
                "confidence": data["conf"][i]
            }
        )


    return results