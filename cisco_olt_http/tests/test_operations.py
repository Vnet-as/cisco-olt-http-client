
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


class TestOperationResult:

    def test_ok_response(self, ok_response):
        operation_result = operations.OperationResult(ok_response)
        assert not operation_result.error
        assert operation_result.error_str == 'OK'
