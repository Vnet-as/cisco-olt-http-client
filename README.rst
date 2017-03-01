
==============
cisco_olt_http
==============


.. image:: https://travis-ci.org/Vnet-as/cisco-olt-http-client.svg?branch=master
   :target: https://travis-ci.org/Vnet-as/cisco-olt-http-client


.. image:: https://codecov.io/gh/Vnet-as/cisco-olt-http-client/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Vnet-as/cisco-olt-http-client


.. image:: https://pyup.io/repos/github/vnet-as/cisco-olt-http-client/shield.svg
   :target: https://pyup.io/repos/github/vnet-as/cisco-olt-http-client/
   :alt: Updates



Usage
=====


.. code-block:: python

    from cisco_olt_http.client import Client
    from cisco_olt_http.operations import (
        BulkOperation,
        ShowInterfacesOp,
        ShowEquipmentOp
    )

    client = Client('https://your.olt.box')
    # unfortunately for now, there's no way to know if login was successful
    client.login('username', 'password')

    response = client.execute(ShowInterfacesOp)
    pprint.pprint(dict(response.operations[0].result))
    pprint.pprint(response.operations[0].error)

    # or

    cmd = ShowInterfacesOp(client)
    response = cmd.execute()
    pprint.pprint(dict(response.operations[0].result))
    pprint.pprint(response.operations[0].error)

    # also bulk operations are supported

    bulk_op = BulkOperation(client)
    bulk_op.add_operation(ShowInterfacesOp, {'@equipmentId': 1})
    bulk_op.add_operation(ShowInterfacesOp, {'@equipmentId': 2})
    bulk_op.add_operation(ShowEquipmentOp)
    response = bulk_op.execute()

    for op in response.operations:
        pprint.pprint(dict(op.result))
