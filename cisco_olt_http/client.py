import logging
import requests
import xmltodict
from urllib.parse import urljoin

LOGGER = logging.getLogger('cisco_olt_http.client')

class Client(object):

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def login(self, username, password):
        login_data = {
            'myusername': username,
            'mypassword': password,
            'button': 'Login', 'textfield': 'UX_EQUIPNAME',
        }
        response = self._req('login.htm', data=login_data)

    def _req(self, url, **options):
        url = urljoin(self.base_url, url)
        LOGGER.debug('Request to: %s with options: %s', url, options)
        response = self.session.post(url, **options)
        LOGGER.debug('Response status: %s content: %s', response.status_code, response.content)
        return response
