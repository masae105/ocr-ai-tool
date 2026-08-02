"""
layout_analyzer.py

OCR座標情報から書類レイアウトを解析する

Lv3 AIレイアウト認識用
"""


def group_by_line(ocr_data, threshold=50):
    """
    OCR結果をY座標ごとにまとめる

    Parameters
    ----------
    ocr_data : list
        extract_data() の結果

    threshold : int
        同じ行と判断するY座標差

    Returns
    -------
    list
        行ごとの文字情報
    """


    lines = []


    # Y座標順に並べる
    sorted_data = sorted(
        ocr_data,
        key=lambda x: x["y"]
    )


    for item in sorted_data:

        added = False


        for line in lines:

            # 同じ高さなら同じ行
            if abs(
                item["y"] - line["y"]
            ) < threshold:

                line["items"].append(item)
                added = True
                break


        # 新しい行
        if not added:

            lines.append(
                {
                    "y": item["y"],
                    "items": [item]
                }
            )


    # 行内の文字をX座標順に並べる
    for line in lines:

        line["items"] = sorted(
            line["items"],
            key=lambda x: x["x"]
        )


        line["text"] = "".join(
            item["text"]
            for item in line["items"]
        )
        
    return lines

def detect_regions(lines, image_height=None):
    """
    OCR行情報から書類領域を判定する

    Lv3 レイアウト認識用

    header:
        上部情報

    detail:
        明細領域

    footer:
        合計・支払情報
    """


    regions = {
        "header": [],
        "detail": [],
        "footer": []
    }


    # 画像高さがない場合
    # OCR全体の最大Yから推測
    if image_height is None:

        max_y = max(
            line["y"]
            for line in lines
        )

        image_height = max_y + 500



    for line in lines:

        y = line["y"]

        # 上部 30%
        if y < image_height * 0.3:

            regions["header"].append(
                line
            )


        # 中央 30〜75%
        elif y < image_height * 0.75:

            regions["detail"].append(
                line
            )


        # 下部
        else:

            regions["footer"].append(
                line
            )


    return regions


    return lines