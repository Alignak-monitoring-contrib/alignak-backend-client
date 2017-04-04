.. _cli:

Backend client CLI
******************

Alignak backend command line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 ``alignak_backend_cli`` is an utility tool that can make simple operations with the Alignak backend.
 It allows getting, updating, creating data from/into the backend.

All the operations that this script permits are strongly related to the Alignak backend data model. Do not even expect dealing with hosts, services, commands, ... if you do not even have the lightest idea of what it is about;)

The Alignak backend data model is defined in the `Alignak backend documentation<http://docs.alignak.net/projects/alignak-backend/en/develop/>`_ and the best source of information is achieved with the `Swagger interface of the backend<http://docs.alignak.net/projects/alignak-backend/en/develop/api.html#browse-alignak-backend-api-swagger>`_. You run the backend and it provides its data model on a Web interface...


Usage
-----
The ``alignak_backend_cli`` script receives some command line parameters to define its behavior:


Command line interface
----------------------
.. automodule:: alignak_backend_client.backend_client


Some examples
-------------

The project repository folder *alignak_backend_client/examples* contains many example files built to be used or thanks to the `alignak-backend-cli` tool.

The following chapters give some command line examples. Do not hesitate to run `alignak-backend-cli -h` for the online help ;)

To have more information about the script execution, use the `-v` / `--verbose` parameter to activate the verbose mode. To test a command before executing operations in the backend, you can use the dry-run mode (`-c` / `--check`).


Add elements
~~~~~~~~~~~~

To add an element (eg. an host named *host_name*) to the backend, run this command:
::

    alignak-backend-cli -t host add host_name

This command will try to add an `host` element named *host_name* into the backend.

**Note** that most of the elements managed by the Alignak backend can be added without specifying any parameters. If some mandatory parameters are required, error message will be raised by the script and the missing parameters will be explained in the messages.


To add an element (eg. an host named *host_name*) to the backend, with some parameters, run this command:
::

    alignak-backend-cli -t host -d data-file.json add host_name

This command will try to add an `host` element named *host_name* into the backend and it will use the parameters contained in the *data-file.json* file. As an example, the file *example_host_data.json* for common configuration parameters or *example_host_livestate.json* for an host live state update.

**Note** that most of the elements managed by the Alignak backend can be added without specifying any parameters. If some mandatory parameters are required, an error message will be raised by the script and the missing parameters will be explained in the messages.


To add a list of elements of a certain type (eg. a list of hosts) into the backend, run this command:
::

    alignak-backend-cli -t host -d data-file.json add

**Note** that the command is the same as for adding an host but the host name is not present!

This command will try to add the `host` elements defined in the *data-file.json* file. This file must contain an array of `host`, each one having a defined `name` property. As an example, the file *example_host_data.json* for common configuration parameters or *example_host_livestate.json* for an host live state update.


Update elements
~~~~~~~~~~~~~~~

To update the elements in the Alignak backend you will use almost the same commands as for adding elements, except that you will use the `update` action word instead of the `add` action word. The provided json data file contains the definition of the properties to update for the targeted element. Using `-i` / `--include-read-data` argument will also update the existing properties that got read when the element was searched before being updated. In some rare situation, it may be necessary to use this argument...

This command will update an host named *host_name*:
::

    alignak-backend-cli -t host -d data-file.json update host_name



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


To get the list of all the services of an host from the backend, run this command:
::

    alignak-backend-cli -t service list host_name/*

This will store the list of all the host *host_name* in a file.


To get an host and the list of all its services, run this command:
::

    alignak-backend-cli -t host get host_name/*

This will store the list of all the host *host_name* in a file.




Delete elements
~~~~~~~~~~~~~~~

To delete the list of all the elements of a certain type (eg. the list of all hosts) from the backend, run this command:
::

    alignak-backend-cli -t host delete

This will delete all the hosts defined in the backend!


To delete all the services related to an host (eg. an host named *host_name*) from the backend, run this command:
::

    alignak-backend-cli -t service delete host_name/*

This will delete all the services linked to the host named *host_name* from the backend.


To delete a specific element (eg. an host named *host_name*) from the backend, run this command:
::

    alignak-backend-cli -t host delete host_name

This will delete the host named *host_name* from the backend.

**Beware** that deleting some elements may create corrupted data in your Alignak backend! Deleting an host without having previously deleted its services will create orphan services that try to be linked to a non-existing host... take care of the deletion order: delete services of an host before the host!



An idea for the Alignak checks packs
------------------------------------

The `alignak-backend-cli` tool allows to mainpulate Alignak backend data. This is the main driver that made an idea raise: why not updating the Alignak backend to install some checks packs?

With the `alignak-backend-cli`, it is easy to add new hosts/ services templates, new commands, new groups, ...

This is the procedure with the examples provided in the project repository folder *alignak_backend_client/examples*. Starting with an empty backend
::

    # Add some commands and templates
    alignak-backend-cli -v -t command -d examples/checks-pack-commands.json add
    alignak-backend-cli -v -t user -d examples/checks-pack-users-templates.json add
    alignak-backend-cli -v -t host -d examples/checks-pack-hosts-templates.json add
    alignak-backend-cli -v -t service -d examples/checks-pack-services-templates.json add

    # Use the Alignak Webui to check the backend content in a friendly manner;)
    # Else:
    alignak-backend-cli -v -t command list
    alignak-backend-cli -v -t user list
    alignak-backend-cli -v -t host -m list
    alignak-backend-cli -v -t service -m list
    # Use the '-m' argument for host and service to get the models (templates)
    # Check the content of the alignak-object-list-*.json files in the current directory
    # As examples, the corresponding files are present in the examples directory, prefixed with checks-pack...

    # Add an host from a template
    alignak-backend-cli -v -t host -T windows-passive-host add host_test

    # Add an host from a template and some more parameters
    alignak-backend-cli -v -t host -d examples/example_host_data.json add host_test_2

    # Get the hosts / services list
    alignak-backend-cli -v -t host list
    alignak-backend-cli -v -t service list
    # As examples, the result files are present in the examples directory:
    # - checks-pack-alignak-object-list-hosts.json
    # - checks-pack-alignak-object-list-services.json



To restart from an empty backend:
::

    $ mongo
    $ use alignak-backend
    $ db.dropDatabase()
    $ Ctrl+C
    $ alignak-backend-uwsgi
