def clean_text(text):

    replacements = {
        "０": "0",
        "１": "1",
        "Ｏ": "O",
        "l": "1",
        "引crosoft": "Microsoft",
        "EdGe": "Edge"
    }


    for old, new in replacements.items():
        text = text.replace(old, new)

    
    # 不要なダブルクォート削除
    text = text.replace('"', '')

    # 前後の空白・改行削除
    text = text.strip()   


    return text