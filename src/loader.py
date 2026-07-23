from pathlib import Path


def load_file(file_path):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"{file_path} が見つかりません"
        )

    print("読み込み成功")
    print("ファイル名:", path.name)
    print("種類:", path.suffix)

    return path