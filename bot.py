import vk_api
import json
from requests_html import HTMLSession

# 1. Reading data for VK session
with open('data_config.json') as json_data:
    vk_data = json.load(json_data)

# # 2. Request to website
# session = HTMLSession()
# r = session.get('http://xn--80aesfpebagmfblc0a.xn--p1ai/')

# # 3. Data parsing from response
# html_table = r.html.find('.d-map__list', first=True)
# data_text = html_table.text.split('\n')
# regions = {item: data_text[i + 1: i + 4]
#            for i, item in enumerate(data_text) if i % 4 == 0}

# 4. VK session and posting
vk_session = vk_api.VkApi(
    login=vk_data['user']['login'],
    token=vk_data['app']['accessToken'],
    app_id=vk_data['app']['clientId'],
    client_secret=vk_data['app']['serviceKey']
)
vk = vk_session.get_api()
print(vk.wall.post(
    message="Hello world",
    owner_id=vk_data['dev_club']['clubNumber'],
    from_group=1
))
