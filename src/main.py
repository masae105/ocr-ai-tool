print("main.py start")


from loader import load_file


def main():

    file_path = "sample_data/images/test.png"

    file = load_file(file_path)

    print("読み込み成功:", file)


if __name__ == "__main__":
    main()