import logging
import requests
import xmltodict
from urllib.parse import urljoin

LOGGER = logging.getLogger('cisco_olt_http.client')


class Operation(object):
    '''Base class for API operations'''

    url = '/cgi-bin/xml-parser.cgi'
    type = 'show'

    def __init__(self, client):
        self.client = client

    def get_base_data(self):
        return {
            'request': {
                'operation': {
                    '@token': self.get_token(),
                    '@type': self.get_type(),
                }
            }
        }

    def get_operation_data(self):
        raise NotImplementedError()

    def get_token(self):
        return self.client.token

    def get_type(self):
        return self.type

    def execute(self):
        response = self.client._req(
            url=self.url,
            data=xmltodict.unparse(self.get_operation_data()))
        return xmltodict.parse(response.content)


class ShowEquipmentOp(Operation):

    def get_operation_data(self, **data):
        base_data = self.get_base_data()
        op_data = {'@entity': 'equipment', 'equipment': {'@id': 0}}
        op_data.update(data)
        base_data['request']['operation'].update(op_data)
        return base_data


class Client(object):

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        # token is incremented before each operation
        self.token = -1

    def login(self, username, password):
        login_data = {
            'myusername': username,
            'mypassword': password,
            'button': 'Login', 'textfield': 'UX_EQUIPNAME',
        }
        response = self._req('login.htm', data=login_data)
        response.raise_for_status()
        return response

    def _op(self, op, incr_token=True):
        if incr_token is True:
            self.token += 1
        return op.execute()

    def _req(self, url, **options):
        url = urljoin(self.base_url, url)
        LOGGER.debug('Request to: %s with options: %s', url, options)
        response = self.session.post(url, **options)
        LOGGER.debug('Response status: %s content: %s', response.status_code, response.content)
        return response
