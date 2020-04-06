import json
import time
from datetime import datetime

from requests_html import HTMLSession
import vk_api

from image_processing import StatisticImage
from errors import error_handler


class Bot:
    def __init__(self):
        self.read_config()
        self._set_next_post_time()

    # @error_handler
    def run(self):
        """ Main function """
        while True:
            if datetime.now() > self.next_post_time:
                self._read_config()
                self._set_next_post_time()
                action = Action(self.DATA)
                action.post_statistic()

            print('Итерация произведена')
            time.sleep(self.DATA['time']['relay_in_seconds'])

    def read_config(self):
        """ Setting DATA """
        with open('data_config.json') as json_data:
            self.DATA = json.load(json_data)

    def _set_next_post_time(self):
        """ Setting the next post time """
        cur_datetime = datetime.now()
        next_hour = datetime(
            cur_datetime.year,
            cur_datetime.month,
            cur_datetime.day,
            cur_datetime.hour + 1
        )

        while next_hour.hour % self.DATA['time']['period_in_hours'] != 0:
            next_hour = next_hour.replace(hour=(next_hour.hour + 1))

        self.next_post_time = next_hour


class Action:
    statistic_url = 'http://xn--80aesfpebagmfblc0a.xn--p1ai/'
    filename = 'image.jpg'

    def __init__(self, data_from_bot):
        self.DATA = data_from_bot
        self.needed_regions = self.DATA['regions']

    def post_statistic(self):
        """ Post statisctic post in vk """
        self._get_request()
        self._parse_statistic_response()
        self._get_vk_api()

        for region in self.needed_regions:
            attachment = self._get_attachment(region)
            self._make_vk_post(attachment)

    def _get_request(self):
        """ Request to website """
        session = HTMLSession()
        self.response = session.get(self.statistic_url)

    def _parse_statistic_response(self):
        """ Data parsing from response """
        html_table = self.response.html.find('.d-map__list', first=True)
        data_text = html_table.text.split('\n')
        self.regions = {item: data_text[i + 1: i + 4]
                        for i, item in enumerate(data_text) if i % 4 == 0}

    def _get_attachment(self, region: str):
        """ Making attachment for VK post """
        vk_upload = vk_api.VkUpload(self.vk)

        image_data = self.DATA['image']
        text_notes = [
            {
                'xy': image_data['xy'][index],
                'text': text_note,
                'font_family': image_data['font_family'],
                'font_size': image_data['font_size'],
                'color': image_data['color']
            } for index, text_note in enumerate(self.regions[region])
        ]

        image_file = StatisticImage(
            self.filename,
            text_notes
        ).make_image()

        photo = vk_upload.photo_wall(
            image_file,
            group_id=self.DATA['dev']['club_number']
        )

        return f"photo{photo[0]['owner_id']}_{photo[0]['id']}"

    def _get_vk_api(self):
        """ Getting VK API """
        vk_session = vk_api.VkApi(
            login=self.DATA['user']['login'],
            token=self.DATA['dev']['access_token'],
            app_id=self.DATA['app']['client_id'],
            client_secret=self.DATA['app']['service_key']
        )
        self.vk = vk_session.get_api()

    def _make_vk_post(self, attachment: str):
        """ Making VK post """
        print(self.vk.wall.post(
            message='ке ллол',
            attachment=attachment,
            owner_id=f"-{self.DATA['dev']['club_number']}",
            from_group=1
        ))
