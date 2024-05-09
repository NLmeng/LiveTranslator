import cv2
import pytesseract


class Preprocessor:
    def __init__(self, image):
        self.image = image
        self.should_deskew = False
        """Use pytesseract OSD to detect orientation and script detection."""
        try:
            self.osd_output = pytesseract.image_to_osd(self.image)
            lines = self.osd_output.split('\n')
            rotate_info = next((line for line in lines if "Rotate" in line), None)
            script_info = next((line for line in lines if "Script" in line), None)

            self.angle = int(rotate_info.split(': ')[1]) if rotate_info else 0
            self.script = script_info.split(': ')[1] if script_info else 'English'

            self.should_deskew = self.angle != 0
        except Exception as e:
            self.angle = 0
            self.script = 'English'
            self.should_deskew = False

    def get_lang_code(self):
        """Use pytesseract OSD to find the main/dominant script and return the three-letter ISO 639-2 code."""
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
        """Gentle noise removal using median blur."""
        return cv2.medianBlur(self.image, 3)

    def deskew(self):
        """Correct skew in images based on OSD orientation angle."""
        if not self.should_deskew:
            return self.image

        rotation_angle = (360 - self.angle) % 360

        (h, w) = self.image.shape[:2]
        center = (w // 2, h // 2)

        rotation_matrix = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)

        abs_cos = abs(rotation_matrix[0, 0])
        abs_sin = abs(rotation_matrix[0, 1])

        new_w = int(h * abs_sin + w * abs_cos)
        new_h = int(h * abs_cos + w * abs_sin)

        rotation_matrix[0, 2] += new_w // 2 - center[0]
        rotation_matrix[1, 2] += new_h // 2 - center[1]

        return cv2.warpAffine(self.image, rotation_matrix, (new_w, new_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    def add_border(self):
        """Add a small border around the image to improve OCR accuracy at edges."""
        border_size = 10  # pixels
        return cv2.copyMakeBorder(self.image, border_size, border_size, border_size, border_size,
                                  cv2.BORDER_CONSTANT, value=[0, 0, 0])

    def process_image(self):
        """Perform all 'necessary' preprocessing steps."""
        image = self.add_border()
        image = self.remove_noise()
        if self.should_deskew:
            image = self.deskew()
        return image
