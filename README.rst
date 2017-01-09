
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
    from cisco_olt_http.operations import ShowInterfacesOp

    client = Client('https://your.olt.box')
    # unfortunately for now, there's no way to know if login was successful
    client.login('username', 'password')

    result = client.execute(ShowInterfacesOp)
    pprint.pprint(dict(result.operation))
    pprint.pprint(result.error)

    # or

    cmd = ShowInterfacesOp(client)
    result = cmd.execute()
    pprint.pprint(dict(result.operation))
    pprint.pprint(result.error)
