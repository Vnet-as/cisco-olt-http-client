
import os
import pytest
import requests
from cisco_olt_http import operations
from cisco_olt_http.client import Client


@pytest.fixture
def data_dir():
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'data'))


@pytest.fixture
def ok_response(data_dir, mocker):
    response = mocker.Mock(autospec=requests.Response)
    with open(os.path.join(data_dir, 'ok_response.xml')) as of:
        response.content = of.read()
    return response


def test_get_data():
    client = Client('http://base-url')
    show_equipment_op = operations.ShowEquipmentOp(client)
    op_data = show_equipment_op.get_data()
    assert op_data


class TestBulkOperation:

    def test_multiple_operations(self):
        client = Client('http://base-url')
        bulk_op = operations.BulkOperation(client)
        bulk_op.add_operation(operations.ShowEquipmentOp)
        bulk_op.add_operation(operations.ShowEquipmentOp,
                              {'@equipmentId': '1'})
        op_data = bulk_op.get_data()
        assert len(op_data['request']['operation']) == 2
        del op_data['request']['operation'][0]['@token']
        ref_data = operations.ShowEquipmentOp(client).get_data()
        del ref_data['request']['operation']['@token']
        assert (op_data['request']['operation'][0] ==
                ref_data['request']['operation'])
        assert op_data['request']['operation'][1]['@equipmentId'] == '1'


class TestOperationResult:

    def test_ok_response(self, ok_response):
        result = operations.Response(ok_response)
        operation_result = result.operations[0]
        assert not operation_result.error
        assert operation_result.error_str == 'OK'
