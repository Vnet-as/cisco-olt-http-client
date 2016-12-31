
from cisco_olt_http import operations
from cisco_olt_http.client import Client


def test_get_data():
    client = Client('http://base-url')
    show_equipment_op = operations.ShowEquipmentOp(client)
    op_data = show_equipment_op.get_data()
    assert op_data
