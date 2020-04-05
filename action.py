from requests_html import HTMLSession
import vk_api

from read_config import DATA
from image_processing import StatisticImage


class Action:
    statistic_url = 'http://xn--80aesfpebagmfblc0a.xn--p1ai/'
    filename = 'image.jpg'

    def __init__(self, needed_regions: list):
        self.needed_regions = needed_regions

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

        image_data = DATA['image']
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
            group_id=DATA['dev']['club_number']
        )

        return f"photo{photo[0]['owner_id']}_{photo[0]['id']}"

    def _get_vk_api(self):
        """ Getting VK API """
        vk_session = vk_api.VkApi(
            login=DATA['user']['login'],
            token=DATA['dev']['access_token'],
            app_id=DATA['app']['client_id'],
            client_secret=DATA['app']['service_key']
        )
        self.vk = vk_session.get_api()

    def _make_vk_post(self, attachment: str):
        """ Making VK post """
        print(self.vk.wall.post(
            message='ке ллол',
            attachment=attachment,
            owner_id=f"-{DATA['dev']['club_number']}",
            from_group=1
        ))
