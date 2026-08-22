import pdf2image
import argparse  # Import the argparse module

def convert_pdf_to_jpg(pdf_file, output_folder="output"):
    """Converts a PDF file to JPG images.

    Args:
        pdf_file (str): Path to the input PDF file.
        output_folder (str, optional): Path to save the output JPGs. Defaults to "output".
    """

    pages = pdf2image.convert_from_path(pdf_file, poppler_path=r"D:\c0dex\python\poppler-23.11.0\Library\bin")

    for i, page in enumerate(pages):
        page.save(f"{output_folder}/page_{i+1}.jpg", "JPEG")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a PDF file to JPG images.')
    parser.add_argument('pdf_file', type=str, help='Path to the input PDF file')
    parser.add_argument('-o', '--output', type=str, default="output",
                        help='Output folder to save the JPG images')
    args = parser.parse_args()

    convert_pdf_to_jpg(args.pdf_file, args.output)