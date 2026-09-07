"""
region_fusion.py

座標判定とキーワード判定の
融合処理（開発中）

Lv3 Step4
"""
def merge_regions(
    coordinate_regions,
    keyword_regions
):
    """
    2種類の領域判定を融合する
    """
    result = {
        "header": [],
        "detail": [],
        "total": [],
        "other": []
    }


    # キーワード判定を優先
    for region, lines in keyword_regions.items():
        for line in lines:
            result[region].append(line)

    return result