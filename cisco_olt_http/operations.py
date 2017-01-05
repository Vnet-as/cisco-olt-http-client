
import xmltodict


class OperationResult:
    '''
    Single operation result class

    Represents XML API response of format like:


    .. code-block:: xml

        <?xml version='1.0' encoding='utf-8'?>
        <response timestamp='1483627466' localDate='2017/01/05'
                  localTime='14:44:26' version='3.6.3-r5162' >
           <operation token='1' type='show' entity='card' >
              <cardList>
                 <card equipmentId='0' id='0' type='0' admin='0' version=''
                       serialNumber='' status='0' hwType='0' hwMode='0'
                       mode='0' name='unknown'>
                 </card>
                 <card equipmentId='0' id='1' type='20213' admin='1' version='PCB 3.2'
                       serialNumber='8010100196' status='3' hwType='20213' hwMode='0'
                       mode='0' name='ME4601-OLT'>
                 </card>
              </cardList>
              <result error='00000000' errorStr='OK'/>
           </operation>
        </response>

    '''

    def __init__(self, response):
        '''
        :param response: requests response class with xml result content
        :type response: :class:`request.Response`
        '''
        #: Raw Http response (:class:`requests.Response`)
        self.response = response
        #: Full, parsed xml from http response
        self.data = xmltodict.parse(response.content)

    @property
    def operation(self):
        return self.data['response']['operation']

    @property
    def result(self):
        return self.operation['result']

    @property
    def error(self):
        return int(self.error_code) != 0

    @property
    def error_code(self):
        return self.result['@error']

    @property
    def error_str(self):
        return self.result['@errorStr']


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
        '''Returns request base data'''
        return {'request': {'operation': self.get_op_base_data()}}

    def get_op_base_data(self):
        '''Returns operation base data'''
        return {
            '@token': self.get_token(),
            '@type': self.get_type(),
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
        '''Get token for the operation'''
        return self.client.token

    def get_type(self):
        '''Get type of operation. ``show``, ``config`` etc.'''
        return self.op_type

    def get_op_data(self):
        '''Returns operation related data bundle'''
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


class ConfigOperation(Operation):
    '''Base class for configuration changing operations'''
    op_type = 'config'


class ShowEquipmentOp(Operation):
    op_data = {'@entity': 'equipment', 'equipment': None}


class ShowInterfacesOp(Operation):
    op_data = {'@entity': 'interface', 'interface': {'@equipmentId': 0}}
