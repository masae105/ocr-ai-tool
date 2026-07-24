from pathlib import Path
from pdf2image import convert_from_path


def pdf_to_images(pdf_path, output_dir):

    output_dir = Path(output_dir)
    output_dir.mkdir(
        exist_ok=True
    )

    images = convert_from_path(
        pdf_path
    )

    image_paths = []
    for i, image in enumerate(images):

        image_path = (
            output_dir / f"page_{i+1}.png"
        )

        image.save(image_path)
        image_paths.append(image_path)

        print("保存:", image_path)


    return image_paths


if __name__ == "__main__":

    pdf_path = "sample_data/pdf/test.pdf"

    output_dir = "output/pdf_images"

    images = pdf_to_images(
        pdf_path,
        output_dir
    )

    print("変換完了")
    print("ページ数:", len(images))