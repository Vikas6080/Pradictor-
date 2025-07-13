import cv2
import pytesseract
import numpy as np

# Configure Tesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

def extract_board_from_image(image_path):
    """Reads the Mines grid from the game screenshot and returns a 5x5 grid of cells."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unreadable.")

    # Resize to fixed size for consistent cell mapping
    image = cv2.resize(image, (500, 500))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Optional: thresholding to improve OCR if needed
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Divide into 5x5 grid
    board = []
    cell_h, cell_w = 100, 100
    for row in range(5):
        row_cells = []
        for col in range(5):
            x1, y1 = col * cell_w, row * cell_h
            cell_img = thresh[y1:y1+cell_h, x1:x1+cell_w]
            text = pytesseract.image_to_string(cell_img, config='--psm 8').strip()
            row_cells.append(text)
        board.append(row_cells)

    return board
