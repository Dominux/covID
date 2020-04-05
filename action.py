from requests_html import HTMLSession
import json
import vk_api

from image_processing import StatisticImage

# TODO Написать метод сборки сообщения и вызывать его в Action._get_statistic_image()


class Action:
    statistic_url = 'http://xn--80aesfpebagmfblc0a.xn--p1ai/'
    filename = 'image.jpg'

    def __init__(self, needed_regions: list):
        self.needed_regions = needed_regions

    def post_statistic(self):
        """ Post statisctic post in vk """
        self._read_config()
        self._get_request()
        self._parse_statistic_response()
        self._get_vk_api()

        for region in self.needed_regions:
            attachment = self._get_attachment(region)
            self._make_vk_post(attachment)

    def _read_config(self):
        """ Reading data for VK session """
        with open('data_config.json') as json_data:
            self.vk_data = json.load(json_data)

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
        """ Making message for VK post """
        vk_upload = vk_api.VkUpload(self.vk)
        image_file = self._get_stastic_image(region)
        photo = vk_upload.photo_wall(
            image_file,
            group_id=self.vk_data['dev']['club_number']
        )
        return f"photo{photo[0]['owner_id']}_{photo[0]['id']}"

    def _get_stastic_image(self, region: str):
        img = StatisticImage(
            self.filename,
            {'xy': (20, 30), 'text': 'skgnd',
             'font_family': 'Inkfree.ttf', 'font_size': 25, 'color': 'red'}
        )
        return img.make_image()

    def _get_vk_api(self):
        """ Getting VK API """
        vk_session = vk_api.VkApi(
            login=self.vk_data['user']['login'],
            token=self.vk_data['dev']['access_token'],
            app_id=self.vk_data['app']['client_id'],
            client_secret=self.vk_data['app']['service_key']
        )
        self.vk = vk_session.get_api()

    def _make_vk_post(self, attachment: str):
        """ Making VK post """
        print(self.vk.wall.post(
            message='ке ллол',
            attachment=attachment,
            owner_id=f"-{self.vk_data['dev']['club_number']}",
            from_group=1
        ))
