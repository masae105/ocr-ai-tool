"""
layout_detector.py

OCR結果と特徴量から請求書レイアウトを判定する
Lv3 Step2
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
    スコアリング方式でレイアウト判定する

    Returns
    -------
    str
        A / B / C / UNKNOWN
    """

    # 空白除去
    text = text.replace(
        " ",
        ""
    ).replace(
        "　",
        ""
    )


    patterns = load_layout_patterns()


    scores = {}


    # 各レイアウトのスコア計算
    for layout, pattern in patterns.items():

        score = 0


        # キーワードスコア
        for keyword, point in pattern["keywords"].items():

            if keyword in text:
                score += point



        # 特徴量スコア
        for feature, point in pattern["features"].items():

            if features.get(feature) is True:

                score += point



        scores[layout] = score


    # 最高スコア取得
    best_layout = max(
        scores,
        key=scores.get
    )


   # スコア順に並べる
    sorted_scores = sorted(
    scores.values(),
    reverse=True
)


    top_score = sorted_scores[0]
    second_score = sorted_scores[1]


    # 信頼度計算
    total_score = sum(scores.values())

    if total_score > 0:
        confidence = top_score / total_score
        
    else:
        confidence = 0

    # 最低スコア判定
    if top_score < 3:
        return "UNKNOWN"


    # 同点判定
    if top_score == second_score:
        return "UNKNOWN"



    return best_layout