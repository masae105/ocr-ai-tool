import pytesseract

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
