from pathlib import Path


def load_file(file_path):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"{file_path} が見つかりません"
        )

    return path