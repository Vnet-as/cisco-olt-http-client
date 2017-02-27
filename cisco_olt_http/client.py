import logging
import requests
import xmltodict

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


LOGGER = logging.getLogger('cisco_olt_http.client')


class Client(object):

    def __init__(self, base_url):
        '''
        :param base_url: OLT box API base url.
        '''
        self.base_url = base_url
        self.session = requests.Session()
        # token is incremented before each operation
        self._token = -1

    @property
    def token(self):
        '''Operation token which is incremented before each use'''
        self._token += 1
        return self._token

    def login(self, username, password):
        '''
        Initiate authenticated session with given credentials

        :param usernam: Username
        :param password: Password

        :returns: Login request's response
        '''
        login_data = {
            'myusername': username,
            'mypassword': password,
            'button': 'Login', 'textfield': 'UX_EQUIPNAME',
        }
        response = self._req('login.htm', data=login_data)
        return response

    def execute(self, op, **kwargs):
        '''
        Execute API request operation with given operation ``data``.

        :param op: Operation class
        :type op: class (type)

        :param data: Operation related data passed
        :type data: dict or None

        :returns: OperationResult
        '''
        return op(self).execute(**kwargs)

    def _req(self, url, method='POST', **options):
        url = urljoin(self.base_url, url)
        LOGGER.debug('Request to: %s with options: %s', url, options)
        response = self.session.request(method, url, **options)
        response.raise_for_status()
        LOGGER.debug(
            'Response status: %s content: %s',
            response.status_code, response.content)
        return response
