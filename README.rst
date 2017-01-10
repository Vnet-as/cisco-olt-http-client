
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

    result = client.execute(ShowInterfacesOp)
    pprint.pprint(dict(result.operations[0]))
    pprint.pprint(result.error)

    # or

    cmd = ShowInterfacesOp(client)
    result = cmd.execute()
    pprint.pprint(dict(result.operations[0]))
    pprint.pprint(result.error)

    # also bulk operations are supported

    bulk_op = BulkOperation(client)
    bulk_op.add_operation(ShowInterfacesOp, {'@equipmentId': 1})
    bulk_op.add_operation(ShowInterfacesOp, {'@equipmentId': 2})
    bulk_op.add_operation(ShowEquipmentOp)
    result = bulk_op.execute()

    pprint.pprint(result.error)
    for res in result.operations:
        pprint.pprint(dict(res))

