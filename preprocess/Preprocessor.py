import cv2
import numpy as np
import pytesseract


class Preprocessor:
    def __init__(self, image):
        self.image = image
        self.should_deskew = False
        self.script = 'English'

    def get_lang_code(self):
        """Use pytesseract OSD to find main/dominant script and return the three-letter ISO 639-2 code."""
        script_to_code = {
            'Japanese': 'jpn',
            'English': 'eng',
            'French': 'fra',
            'Latin': 'eng',
        }
        return script_to_code.get(self.script, 'eng')

    def get_grayscale(self):
        """Convert to grayscale."""
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def remove_noise(self):
        """Noise removal using median blur."""
        return cv2.medianBlur(self.image, 5)

    def detect_orientation(self):
        """Use pytesseract OSD to detect orientation and script detection."""
        osd_output = pytesseract.image_to_osd(self.image)
        lines = osd_output.split('\n')
        rotate_info = [line for line in lines if "Rotate" in line][0]
        self.script = [line for line in lines if "Script" in line][0].split(': ')[
            1]
        angle = int(rotate_info.split(': ')[1])
        if angle != 0:
            self.should_deskew = True
        return angle

    def deskew(self):
        """Correct skew in images if orientation is detected as non-zero."""
        if not self.should_deskew:
            return self.image
        gray = self.get_grayscale()
        coords = np.column_stack(np.where(gray > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = gray.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(gray, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    def add_border(self):
        """Add a small border around the image to improve OCR accuracy at edges."""
        border_size = 10  # pixels
        return cv2.copyMakeBorder(self.image, border_size, border_size, border_size, border_size,
                                  cv2.BORDER_CONSTANT, value=[0, 0, 0])

    def process_image(self):
        """Perform all 'necessary' preprocessing steps."""
        self.image = self.add_border()
        self.detect_orientation()
        image = self.remove_noise()
        if self.should_deskew:
            image = self.deskew()
        return image
