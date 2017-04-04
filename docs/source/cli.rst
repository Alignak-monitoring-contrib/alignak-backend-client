.. _cli:

Backend client CLI
******************

Alignak backend command line interface
======================================

``alignak_backend_cli`` is an utility tool that can make simple operations with the Alignak backend. It allows getting, updating, creating data from/into the backend.

All the operations that this script permits are strongly related to the Alignak backend data model. Do not even expect dealing with hosts, services, commands, ... if you do not even have the lightest idea of what it is about;)

The Alignak backend data model is defined in the `Alignak backend documentation`_ and the best source of information is achieved with the `Swagger interface of the backend`_. You run the backend and it provides its data model on a Web interface...

.. _Alignak backend documentation: http://docs.alignak.net/projects/alignak-backend/en/develop/
.. _Swagger interface of the backend: http://docs.alignak.net/projects/alignak-backend/en/develop/api.html#browse-alignak-backend-api-swagger


Usage
=====
The ``alignak_backend_cli`` script receives some command line parameters to define its behavior:


Command line interface
----------------------
alignak-backend-cli command line interface:
::

    Usage:
        alignak-backend-cli [-h]
        alignak-backend-cli [-V]
        alignak-backend-cli [-v] [-q] [-c] [-l] [-m] [-e] [-i]
                            [-b=url] [-u=username] [-p=password]
                            [-d=data]
                            [-f=folder]
                            [-T=template] [-t=type] [<action>] [<item>]

    Options:
        -h, --help                  Show this screen.
        -V, --version               Show application version.
        -v, --verbose               Run in verbose mode (more info to display)
        -q, --quiet                 Run in quiet mode (display nothing)
        -c, --check                 Check only (dry run), do not change the backend.
        -l, --list                  Get an items list
        -b, --backend url           Specify backend URL [default: http://127.0.0.1:5000]
        -u, --username=username     Backend login username [default: admin]
        -p, --password=password     Backend login password [default: admin]
        -d, --data=data             Data for the new item to create [default: none]
        -f, --folder=folder         Folder where to read/write data files [default: none]
        -i, --include-read-data     Do not use only the provided data, but append the one
                                    read from he backend
        -t, --type=host             Type of the provided item [default: host]
        -e, --embedded              Do not embed linked objects
        -m, --model                 Get only the templates
        -T, --template=template     Template to use for the new item

    Exit code:
        0 if required operation succeeded
        1 if backend access is denied (check provided username/password)
        2 if element operation failed (missing template,...)

        64 if command line parameters are not used correctly

    Use cases:
        Display help message:
            alignak-backend-cli (-h | --help)

        Display current version:
            alignak-backend-cli -V
            alignak-backend-cli --version

        Specify backend parameters if they are different from the default
            alignak-backend-cli -b=http://127.0.0.1:5000 -u=admin -p=admin get host_name

    Actions:
        'get' to get an item in the backend
        'list' (shortcut for 'get -l' to get the list of all items of a type
        'add' to add an(some) item(s) in the backend
        'update' to update an(some) item(s) in the backend
        'delete' to delete an item (or all items of a type) in the backend

    Use cases to get data:
        Get an items list from the backend:
            alignak-backend-cli get -l
            Try to get the list of all hosts and copy the JSON dump in a file named
            './alignak-object-list-hosts.json'

            alignak-backend-cli get -l -t user
            Try to get the list of all users and copy the JSON dump in a file named
            './alignak-object-list-users.json'

            alignak-backend-cli get -l -f /tmp -t user
            Try to get the list of all users and copy the JSON dump in a file named
            '/tmp/alignak-object-list-users.json'

            alignak-backend-cli list -t user
            Shortcut for 'alignak-backend-cli get -l -t user'

        Get the hosts templates list from the backend:
            alignak-backend-cli -l -m
            Try to get the list of all hosts templates and copy the JSON dump in a
            file named './alignak-object-list-hosts.json'

        Get an item from the backend:
            alignak-backend-cli get host_name
            Try to get the definition of an host named 'host_name' and copy the JSON dump
            in a file named './alignak-object-dump-host-host_name.json'

            alignak-backend-cli -t user get contact_name
            Try to get the definition of a user (contact) contact named 'contact_name' and
            copy the JSON dump in a file named './alignak-object-dump-contact-contact_name.json'

        Get a service from the backend:
            alignak-backend-cli get -t service host_name/service_name
            Try to get the definition of the service service_name for an host named 'host_name'
            and copy the JSON dump in a file named
            './alignak-object-dump-service-host_name_service_name.json'

    Use cases to add data:
        Add an item to the backend (without templating):
            alignak-backend-cli new_host
            This will add an host named new_host

            alignak-backend-cli -t user new_contact
            This will add a user named new_contact

        Add an item to the backend (with some data):
            alignak-backend-cli --data="/tmp/input_host.json" add new_host
            This will add an host named new_host with the data that are read from the
            JSON file /tmp/input_host.json

            alignak-backend-cli -t user new_contact --data="stdin"
            This will add a user named new_contact with the JSON data read from the
            stdin. You can 'cat file > alignak-backend-cli -t user new_contact --data="stdin"'

        Add an item to the backend based on a template:
            alignak-backend-cli -T host_template add new_host
            This will add an host named new_host with the data existing in the template
            host_template

        Add an item to the backend based on several templates:
            alignak-backend-cli -T "host_template,host_template2" add new_host
            This will add an host named new_host with the data existing in the templates
            host_template and host_template2

    Use cases to update data:
        Update an item into the backend (with some data):
            alignak-backend-cli --data="./update_host.json" update test_host
            This will update an host named test_host with the data that are read from the
            JSON file ./update_host.json

    Use cases to delete data:
        Delete an item from the backend:
            alignak-backend-cli delete test_host
            This will delete the host named test_host

        Delete all items from the backend:
            alignak-backend-cli delete -t retentionservice
            This will delete all the retentionservice items

        Delete all the services of an host from the backend:
            alignak-backend-cli delete -t service test_host/*
            This will delete all the services of the host named test_host

    Hints and tips:
        You can operate on any backend endpoint: user, host, service, graphite, ... see the
        Alignak backend documentation (http://alignak-backend.readthedocs.io/) to get a full
        list of the available endpoints and their data fields.

        For a service specify the name as 'host_name/service_name' to get a service for a
        specific host, else the script will return the first serice with the required name

        By default, the script embeds in the provided result all the possible embeddable data.
        As such, when you get a service, you will also get its host, check period, ...
        Unfortunately, the same embedding can not be used when adding or updating an item :(

        Use the -m (--model) option to get the templates lists for the host, service or user
        when you get a list. If not used, the list do not include the templates

        Use the -e (--embedded) option to get the linked objects embedded in the output. For
        an host, as an example, the result will include the linked check period, contacts,
        check command,... If not used, the result will only include the linked objects identifier.

        To get the list of all the services of an host, you can get the service list with
        a wildcard in the host name. For all the services of the host named 'passive-01',
        use 'passive-01/*' as in 'alignak-backend-cli get -l -t service passive-01/*'

        To get all the information for an host, including the services, you can use
        a wildcard in the host name. For all the information of the host named 'passive-01',
        use 'passive-01/*' as in 'alignak-backend-cli get -t host passive-01/*'. Using the -e
        option will include all the related objects of the host and its services in the
        dump file.

        If somehow you need to update an item and post all the data when updating, use the
        `-i` option. This will use the data read from the backend and update this data with
        the one provided in the data file specified in the `-d` option.

        Use the -v option to have more information


**Note**: this is not automatically updated from the source code. To get the most recent version, run `alignak-backend-cli -h`!

Some examples
=============

The project repository folder *alignak_backend_client/examples* contains many example files built to be used or thanks to the `alignak-backend-cli` tool.

The following chapters give some command line examples. Do not hesitate to run `alignak-backend-cli -h` for the online help ;)

To have more information about the script execution, use the `-v` / `--verbose` parameter to activate the verbose mode. To test a command before executing operations in the backend, you can use the dry-run mode (`-c` / `--check`).


Add elements
------------

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
---------------

To update the elements in the Alignak backend you will use almost the same commands as for adding elements, except that you will use the `update` action word instead of the `add` action word. The provided json data file contains the definition of the properties to update for the targeted element. Using `-i` / `--include-read-data` argument will also update the existing properties that got read when the element was searched before being updated. In some rare situation, it may be necessary to use this argument...

This command will update an host named *host_name*:
::

    alignak-backend-cli -t host -d data-file.json update host_name



Get elements
------------

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
---------------

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



An idea / some tests for the Alignak checks packs
=================================================

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
