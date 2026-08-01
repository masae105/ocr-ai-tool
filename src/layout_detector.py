"""
layout_detector.py

OCR結果と特徴量から請求書レイアウトを判定する
Lv3 Step1
"""

import json
import os


PATTERN_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "layout_patterns.json"
)


def load_layout_patterns():
    """
    レイアウト判定パターン読み込み
    """

    with open(
        PATTERN_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)



def detect_layout(text, features):
    """
    OCR結果と特徴量から
    請求書レイアウトを判定する
    """

    text = text.replace(" ", "").replace("　", "")

    patterns = load_layout_patterns()


    for layout, pattern in patterns.items():

        # キーワード一致数
        keyword_match = sum(
            keyword in text
            for keyword in pattern["keywords"]
        )


        # 特徴一致数
        feature_match = 0

        for key, value in pattern["features"].items():

            if features.get(key) == value:
                feature_match += 1


        # 判定条件
        if keyword_match >= 1 and feature_match >= 1:
            return layout


    return "UNKNOWN"