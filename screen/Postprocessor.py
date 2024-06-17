import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class Postprocessor:
    def __init__(self, font_path="arial.ttf", font_size=20):
        self.font_path = font_path
        self.font_size = font_size

    def get_image_from_path(self, image_path):
        """Load an image from a given file path and convert it to RGB."""
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def blur_background(self, frame, box):
        """Apply a blur effect to the background of a bounding box."""
        x, y, w, h = box
        blurred_box = cv2.GaussianBlur(
            frame[y:y+h, x:x+w], (15, 15), cv2.BORDER_DEFAULT)
        frame[y:y+h, x:x+w] = blurred_box
        return frame

    def wrap_text(self, text, max_width, font):
        """Wraps the text to fit within the specified max_width using the provided font."""
        lines = []
        words = text.split()

        while words:
            line = ''
            while words and font.getbbox(line + words[0])[2] <= max_width:
                line += (words.pop(0) + ' ')

            if not line and words:
                long_word = words.pop(0)
                for i in range(len(long_word)):
                    if font.getbbox(line + long_word[i])[2] <= max_width:
                        line += long_word[i]
                    else:
                        if line:
                            lines.append(line)
                            line = long_word[i]
                        else:
                            line += long_word[i]
                if line:
                    lines.append(line)
                continue

            if line:
                lines.append(line.strip())

        return lines

    def put_text_on_frame(self, frame, text, box, draw_box=False):
        """Put text on the frame image with a blurred background for the text box and optionally draw the bounding box."""
        x, y, w, h = box

        sub_frame = frame[y:y+h, x:x+w]
        sub_frame = self.blur_background(sub_frame, (0, 0, w, h))

        if draw_box:
            cv2.rectangle(sub_frame, (0, 0), (w, h), (0, 255, 0), 2)

        try:
            font = ImageFont.truetype(self.font_path, self.font_size)
        except IOError:
            font = ImageFont.load_default()

        wrapped_text = self.wrap_text(text, w, font)

        pil_image = Image.fromarray(sub_frame)
        draw = ImageDraw.Draw(pil_image)

        line_height = font.getbbox('A')[3] - font.getbbox('A')[1]
        total_text_height = line_height * len(wrapped_text)
        if total_text_height > h:
            font_size = int(h / len(wrapped_text))
            try:
                font = ImageFont.truetype(self.font_path, font_size)
            except IOError:
                font = ImageFont.load_default()
            line_height = font.getbbox('A')[3] - font.getbbox('A')[1]

        text_color = (255, 255, 255) if np.mean(sub_frame) < 128 else (0, 0, 0)

        for i, line in enumerate(wrapped_text):
            text_width, text_height = font.getbbox(line)[2:4]
            text_x = (w - text_width) // 2
            text_y = i * line_height
            draw.text((text_x, text_y), line, font=font, fill=text_color)

        frame[y:y+h, x:x+w] = np.array(pil_image)

        return frame

    def draw_bounding_boxes(self, image, bounding_boxes):
        """Draw bounding boxes on the image to visualize the segmentation."""
        for box in bounding_boxes:
            x, y, w, h = box
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return image
