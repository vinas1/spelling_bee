import argparse
import pdf2image
from PIL import Image

def convert_pdf_to_long_jpg(pdf_file, output_file="output.jpg"):
    pages = pdf2image.convert_from_path(pdf_file, poppler_path=r"D:\c0dex\python\poppler-23.11.0\Library\bin")

    # Get dimensions of the first page (assuming all pages are the same size)
    page_width, page_height = pages[0].size

    # Calculate total height for the long image
    total_height = page_height * len(pages)

    # Create a new long image
    long_image = Image.new('RGB', (page_width, total_height))

    # Paste pages into the long image
    y_offset = 0
    for page in pages:
        long_image.paste(page, (0, y_offset))
        y_offset += page_height

    long_image.save(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a PDF file to a long JPG image.')
    parser.add_argument('pdf_file', type=str, help='Path to the input PDF file')
    parser.add_argument('-o', '--output', type=str, default="output.jpg",
                        help='Output file name for the long image')
    args = parser.parse_args()

    convert_pdf_to_long_jpg(args.pdf_file, args.output)
