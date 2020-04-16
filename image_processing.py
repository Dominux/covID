from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


class StatisticImage:
    IMAGES_DIR = 'static/images/'
    FONTS_DIR = 'static/fonts/'

    def __init__(self, image_data, region, text_notes):
        """
        :param image_data:  Image data
        :param region: Region name
        :param text_notes:  Datalist
        """
        self.image_data = image_data
        self.region = region
        self.text_notes = text_notes

        self.numbers_font = ImageFont.truetype(
            f"{self.FONTS_DIR}{image_data['font_file']}",
            size=image_data['numbers']['font_size']
        )
        self.region_name_font = ImageFont.truetype(
            f"{self.FONTS_DIR}{image_data['font_file']}",
            size=image_data['region_name']['font_size']
        )

        self.image_file = Image.open(
            f"{self.IMAGES_DIR}{image_data['filename']}")
        self.image = ImageDraw.Draw(self.image_file)

    def make_image(self):
        """ Main method """
        self.image.multiline_text(
            xy=self.image_data['region_name']['xy'],
            text='\n'.join(self.region.split()),
            font=self.region_name_font,
            fill=self.image_data['color'],
            align='center'
        )

        for index, text_note in enumerate(self.text_notes):
            self.image.text(
                xy=self.image_data['numbers']['xy'][index],
                text=text_note,
                font=self.numbers_font,
                fill=self.image_data['color']
            )

        img_buffer = BytesIO()
        self.image_file.save(img_buffer, 'JPEG')
        img_buffer.seek(0)
        return img_buffer
