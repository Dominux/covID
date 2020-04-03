from requests_html import HTMLSession


class Action:
    def __init__(self, needed_regions: list):
        self.needed_regions = needed_regions

    def execute(self):
        """ Main method """
        self._read_config()
        self._get_request()
        self._parse_response()

        for region in self.needed_regions:
            message = self._make_message(region)
            self._make_vk_post(message)

    def _read_config(self):
        """ Reading data for VK session """
        import json

        with open('data_config.json') as json_data:
            self.vk_data = json.load(json_data)

    def _get_request(self):
        """ Request to website """
        session = HTMLSession()
        self.response = session.get('http://xn--80aesfpebagmfblc0a.xn--p1ai/')

    def _parse_response(self):
        """ Data parsing from response """
        html_table = self.response.html.find('.d-map__list', first=True)
        data_text = html_table.text.split('\n')
        self.regions = {item: data_text[i + 1: i + 4]
                        for i, item in enumerate(data_text) if i % 4 == 0}

    def _make_message(self, region: str):
        """ Making message for VK post """
        print(region)
        print(self.regions[region])
        message = f"{region} - {self.regions[region]}"
        return message

    def _make_vk_post(self, message: str):
        """ Making VK post """
        import vk_api

        vk_session = vk_api.VkApi(
            login=self.vk_data['user']['login'],
            token=self.vk_data['app']['accessToken'],
            app_id=self.vk_data['app']['clientId'],
            client_secret=self.vk_data['app']['serviceKey']
        )
        vk = vk_session.get_api()
        print(vk.wall.post(
            message=message,
            owner_id=self.vk_data['dev_club']['clubNumber'],
            from_group=1
        ))
