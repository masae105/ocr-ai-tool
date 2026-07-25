from PIL import Image, ImageFilter


def preprocess_image(image):

    # グレースケール
    image = image.convert("L")

     # 画像拡大
    image = image.resize((image.width * 2, image.height * 2))

    # 二値化
    image = image.point(lambda  x: 0 if x < 180 else 255)

    # ノイズ除去
    image = image.filter(ImageFilter.MedianFilter())


    return image