# Spelling Bee 🐝🐝🐝

A Python-based Spelling Bee program.

## Description
This project provides a Spelling Bee application with multiple versions. It includes tools for word management and PDF processing utilities.

## Project Structure
- `spelling_bee*.py`: Main application scripts (versions 2.0 and 2.1).
- `words.txt`: The word list used by the program.
- `version.txt`: Current version information.
- `pdftojpg.py` & `PDFtoLongJPG.py`: Utilities to convert PDFs to images.
- `dist/`: Pre-built executable binaries for quick start.

## How to Run

### Using Pre-built Executables
You can find the pre-built `.exe` files in the `dist/` folder. Simply run:
- `spelling_bee2.0.exe`
- `spelling_bee2.1.exe`

> if you create a words.txt file in the same folder, spelling_bee will use it!

### Running from Source
1. Ensure you have Python installed.
2. Install any required dependencies (if applicable).
3. Run the desired version:
   ```bash
   python spelling_bee2.1.py
   ```

## Development
The project uses PyInstaller to create the executables. Spec files (`*.spec`) are provided for build configuration.

## License
Apache 2.0
