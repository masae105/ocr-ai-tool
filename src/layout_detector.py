"""
layout_detector.py

OCR結果から請求書レイアウトを判定する
Lv3 Step1
"""


def detect_layout(text):
    """
    OCRテキストから請求書レイアウトを判定する

    Returns
    -------
    str
        "A" : A形式
        "B" : B形式
        "UNKNOWN" : 判定不可
    """

    text = text.replace(" ", "").replace("　", "")

    
    # A形式
    # 請求番号形式
    a_keywords = [
        "請求番号",
        "株式会社ABC",
    ]

   
    # B形式
    # 請求No + 消費税形式
    b_keywords = [
        "請求No",
        "株式会社XYZ",
    ]

    # C形式
    # サンプル商事形式
    c_keywords = [
        "サンプル商事",
        "USBメモリ",
        "Webカメラ",
    ]

    if any(keyword in text for keyword in a_keywords):
        return "A"

    if any(keyword in text for keyword in b_keywords):
        return "B"

    if any(keyword in text for keyword in c_keywords):
        return "C"

    return "UNKNOWN"