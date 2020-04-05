from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


class StatisticImage:
    IMAGES_DIR = 'static/images/'
    FONTS_DIR = 'static/fonts/'

    def __init__(self, filename, *text_notes):
        """
        :param filename (str):  Name of the image file
        :param text_notes (list):  Text description in format: { 
            'xy': (x, y) (int), 
            'text': (str), 
            'font_family': (str), 
            'font_size': (int), 
            'color': (str)
            }
        """
        self.text_notes = text_notes
        self.image_file = Image.open(f'{self.IMAGES_DIR}{filename}')
        self.image = ImageDraw.Draw(self.image_file)

    def make_image(self):
        """ Main function """
        for text_note in self.text_notes:
            current_font = f"{self.FONTS_DIR}{text_note['font_family']}"
            font = ImageFont.truetype(
                current_font, size=text_note['font_size'])
            self.image.text(
                xy=text_note['xy'],
                text=text_note['text'],
                font=font,
                fill=text_note['color']
            )
        img_buffer = BytesIO()
        self.image_file.save(img_buffer, 'JPEG')
        img_buffer.seek(0)
        return img_buffer
