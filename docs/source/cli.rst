.. _cli:

Backend client CLI
******************

Alignak backend command line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 ``alignak_backend_cli`` is an utility tool that can make simple operations with the Alignak backend.
 It allows getting, updating, creating data from/into the backend.


Usage
-----
The ``alignak_backend_cli`` script receives some command line parameters to define its behavior:


Command line interface
----------------------
.. automodule:: alignak_backend_client.backend_client


Some examples
-------------

The project repository folder *alignak_backend_client/examples* contains many example files built thanks to the `alignak-backend-cli` tool.

The following chapters give some command line examples. Do not hesitate to run `alignak-backend-cli -h` for the online help ;)

To have more information about the script execution, use the `-v` parameter to activate the verbose mode.


Add elements
~~~~~~~~~~~~

To add an element (eg. an host named *host_name*) to the backend, run this command:
::

    alignak-backend-cli -t host add host_name

This command will try to add an `host` element named *host_name* into the backend.

**Note** that most of the elements managed by the Alignak backend can be added without specifying any parameters. If some mandatory parameters are required, error message will be raised by the script and the missing parameters will be explained in the messages.


To add an element (eg. an host named *host_name*) to the backend, with some parameters, run this command:
::

    alignak-backend-cli -t host add host_name

This command will try to add an `host` element named *host_name* into the backend.

**Note** that most of the elements managed by the Alignak backend can be added without specifying any parameters. If some mandatory parameters are required, error message will be raised by the script and the missing parameters will be explained in the messages.


To get the list of all the elements of a certain type (eg. the list of all hosts) from the backend, run this command:
::

    alignak-backend-cli -t host list

This will store the result in a file named *alignak-object-list-hosts.json* in the current directory. Adding the `-e` parameter to the command line will also get the linked elements for each element of the list (eg. the commands, timeperiods, ... linked to each host).


Get elements
~~~~~~~~~~~~

To get the list of all the elements of a certain type (eg. the list of all hosts) from the backend, run this command:
::

    alignak-backend-cli -t host list

This will store the result in a file named *alignak-object-list-hosts.json* in the current directory. Adding the `-e` parameter to the command line will also get the linked elements for each element of the list (eg. the commands, timeperiods, ... linked to each host).


To get a specific element (eg. an host named *host_name*) from the backend, run this command:
::

    alignak-backend-cli -t host get host_name

This will store the result in a file named *alignak-object-dump-host-host_name.json* in the current directory. As for the list, the `-e` parameter will embed the linked elements.

