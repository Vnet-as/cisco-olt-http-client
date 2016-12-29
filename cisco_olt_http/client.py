import logging
import requests
import xmltodict
from urllib.parse import urljoin


LOGGER = logging.getLogger('cisco_olt_http.client')


class Client(object):

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        # token is incremented before each operation
        self._token = -1

    @property
    def token(self):
        self._token += 1
        return self._token

    def login(self, username, password):
        login_data = {
            'myusername': username,
            'mypassword': password,
            'button': 'Login', 'textfield': 'UX_EQUIPNAME',
        }
        response = self._req('login.htm', data=login_data)
        return response

    def _req(self, url, **options):
        url = urljoin(self.base_url, url)
        LOGGER.debug('Request to: %s with options: %s', url, options)
        response = self.session.post(url, **options)
        response.raise_for_status()
        LOGGER.debug(
            'Response status: %s content: %s',
            response.status_code, response.content)
        return response
