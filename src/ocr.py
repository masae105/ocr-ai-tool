import pytesseract
from PIL import Image

# Tesseractの場所を指定
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text(image_path):
    """
    画像から文字を抽出する
    """

    image = Image.open(image_path)

    text = pytesseract.image_to_string(
        image,
        lang="jpn"
    )

    return text

if __name__ == "__main__":

    image_path = "sample_data/images/test.png"

    result = extract_text(image_path)

    print(result)