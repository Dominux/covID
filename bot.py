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
        """ Main method """
        while True:
            if datetime.now() > self.next_post_time or self.DATA['env'] == 'dev':
                self.read_config()
                self._set_next_post_time()
                action = Action(self.DATA)
                action.post_statistic()

            print(f"{datetime.now().time()} - Bot is running")
            time.sleep(self.DATA['info']['relay_in_seconds'])

    def read_config(self):
        """ Setting DATA """
        with open('data_config.json', encoding='utf-8') as json_data:
            data = json.load(json_data)

        data['info'] = data[data['env']]
        del data['dev']
        del data['prod']

        self.DATA = data

    def _set_next_post_time(self):
        """ Setting the next post time """
        cur_datetime = datetime.now()

        # Expected sorted time_points
        time_points = [datetime(
            cur_datetime.year,
            cur_datetime.month,
            cur_datetime.day,
            int(time_point[0]),
            int(time_point[1]),
        ) for time_point in self.DATA['info']['time_points']]

        self.next_post_time = time_points[0]

        for time_point in time_points:
            if time_point > cur_datetime:
                self.next_post_time = time_point
                break


class Action:
    """
        One bot action (iteration)

        Main method - Action.post_statistic()

    """

    def __init__(self, data_from_bot):
        self.DATA = data_from_bot
        self.clubs = self.DATA['info']['clubs']

    def post_statistic(self):
        """ Post statisctic posts in all vk clubs """
        self._get_request()
        self._parse_statistic_response()
        self._get_vk_api()

        for club in self.clubs:
            attachment = self._get_attachment(club)
            self._make_vk_post(club, attachment)

    def _get_request(self):
        """ Request to website """
        session = HTMLSession()
        self.response = session.get(self.DATA['statistic_website'])

    def _parse_statistic_response(self):
        """ Data parsing from response """
        html_table = self.response.html.find('.d-map__list', first=True)
        data_text = html_table.text.split('\n')
        self.regions_info = {item: data_text[i + 1: i + 4]
                             for i, item in enumerate(data_text) if i % 4 == 0}

        html_rus_results = self.response.html.find(
            '.d-map__counter', first=True).find('h3')
        self.rus_info = [_.text.split('+')[0] for _ in html_rus_results]

    def _get_attachment(self, club):
        """ Making attachment for VK post """
        vk_upload = vk_api.VkUpload(self.vk)

        text_notes = self.regions_info[club['region']] + self.rus_info
        image_file = StatisticImage(
            self.DATA['image'],
            club['region'],
            text_notes
        ).make_image()

        photo = vk_upload.photo_wall(image_file, group_id=club['club_id'])

        return f"photo{photo[0]['owner_id']}_{photo[0]['id']}"

    def _get_vk_api(self):
        """ Getting VK API """
        vk_session = vk_api.VkApi(
            login=self.DATA['info']['user']['login'],
            token=self.DATA['info']['app']['access_token'],
            app_id=self.DATA['info']['app']['client_id'],
            client_secret=self.DATA['info']['app']['service_key']
        )
        self.vk = vk_session.get_api()

    def _make_vk_post(self, club, attachment: str):
        """ Making VK post """
        post_id = self.vk.wall.post(
            message='ке ллол',
            attachment=attachment,
            owner_id=f"-{club['club_id']}",
            from_group=1
        )['post_id']

        print(f"{self.DATA['post_url']}{club['club_id']}_{post_id}")
