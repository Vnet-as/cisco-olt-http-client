
import xmltodict


class OperationResult:

    def __init__(self, response):
        self.response = response
        self.data = xmltodict.parse(response.content)

    @property
    def error(self):
        return int(self.error_code) != 0

    @property
    def error_code(self):
        return self.data['response']['operation']['result']['error']


class Operation(object):
    '''Base class for API operations'''

    #: Relative url to the client's ``base_url``. Operation endpoint url
    url = '/cgi-bin/xml-parser.cgi'

    #: Operation type (`show`, `config`, etc)
    op_type = 'show'

    #: Operation specific data bundle
    op_data = {}

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

    def get_data(self, data=None):
        '''
        Merges operation base data structure with operation related one and
        returns the whole bundle which, after serializing to xml can be used
        for operation request.

        :param data: Data to merge with operation data
        :type data: dict

        :returns: full operation data structure
        '''
        base_data = self.get_base_data()
        op_data = self.get_op_data()
        op_data.update(data if data else {})
        base_data['request']['operation'].update(op_data)
        return base_data

    def get_token(self):
        return self.client.token

    def get_type(self):
        return self.op_type

    def get_op_data(self):
        return self.op_data.copy()

    def execute(self, data=None):
        '''
        Execute API request operation with given operation ``data``

        :param data: Operation related data pased to ``get_data`` method
        :type data: dict or None

        :returns: Parsed API response as dictionary
        '''
        response = self.client._req(
            url=self.url,
            data=xmltodict.unparse(self.get_data(data=data)))
        return OperationResult(response)


class ShowEquipmentOp(Operation):
    op_data = {'@entity': 'equipment', 'equipment': None}