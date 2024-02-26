Example schema
==============

.. tab-set::

    .. tab-item:: Rendered using sphinx-jsonschema

        .. jsonschema:: ../schema/server/events/kernel-actions/v1/kernel-actions.schema.json

    .. tab-item:: JSON

        .. literalinclude:: ../schema/server/events/kernel-actions/v1/kernel-actions.schema.json
           :language: JSON

    .. tab-item:: TOML

        .. code-block:: toml

            "$schema" = "https://json-schema.org/draft/2020-12/schema"
            "$id" = "https://schema.jupyter.org/server/events/kernel-actions/v1/kernel-actions.schema.json"
            version = 1
            title = "Kernel Manager activities"
            personal-data = true
            description = "Record events of a kernel manager.\n"
            type = "object"
            required = [ "action", "msg",]

            [properties.action]
            enum = [ "start", "interrupt", "shutdown", "restart",]
            description = "Action performed by the Kernel Manager.\n\nThis is a required field.\n\nPossible values:\n\n1. start\n   A kernel has been started with the given kernel id.\n\n2. interrupt\n   A kernel has been interrupted for the given kernel id.\n\n3. shutdown\n   A kernel has been shut down for the given kernel id.\n\n4. restart\n   A kernel has been restarted for the given kernel id.\n"

            [properties.kernel_id]
            type = "string"
            description = "Kernel id.\n\nThis is a required field for all actions and statuses except action start with status error.\n"

            [properties.kernel_name]
            type = "string"
            description = "Name of the kernel.\n"

            [properties.status]
            enum = [ "error", "success",]
            description = "Status received from a rest api operation to kernel server.\n\nThis is a required field.\n\nPossible values:\n\n1. error\n   Error response from a rest api operation to kernel server.\n\n2. success\n   Success response from a rest api operation to kernel server.\n"

            [properties.status_code]
            type = "number"
            description = "Http response codes from a rest api operation to kernel server.\nExamples: 200, 400, 502, 503, 599 etc\n"

            [properties.msg]
            type = "string"
            description = "Description of the event specified in action.\n"

            [if.not.properties.status]
            const = "error"

            [if.not.properties.action]
            const = "start"

            [then]
            required = [ "kernel_id",]

    .. tab-item:: YAML

        .. code-block:: yaml

            $schema: https://json-schema.org/draft/2020-12/schema
            $id: https://schema.jupyter.org/server/events/kernel-actions/v1/kernel-actions.schema.json
            version: 1
            title: Kernel Manager activities
            personal-data: true
            description: 'Record events of a kernel manager.

            '
            type: object
            required:
            - action
            - msg
            properties:
            action:
                enum:
                - start
                - interrupt
                - shutdown
                - restart
                description: "Action performed by the Kernel Manager.\n\nThis is a required field.\n\nPossible values:\n\
                \n1. start\n   A kernel has been started with the given kernel id.\n\n2. interrupt\n   A kernel\
                \ has been interrupted for the given kernel id.\n\n3. shutdown\n   A kernel has been shut down for\
                \ the given kernel id.\n\n4. restart\n   A kernel has been restarted for the given kernel id.\n"
            kernel_id:
                type: string
                description: 'Kernel id.


                This is a required field for all actions and statuses except action start with status error.

                '
            kernel_name:
                type: string
                description: 'Name of the kernel.

                '
            status:
                enum:
                - error
                - success
                description: "Status received from a rest api operation to kernel server.\n\nThis is a required field.\n\
                \nPossible values:\n\n1. error\n   Error response from a rest api operation to kernel server.\n\n\
                2. success\n   Success response from a rest api operation to kernel server.\n"
            status_code:
                type: number
                description: 'Http response codes from a rest api operation to kernel server.

                Examples: 200, 400, 502, 503, 599 etc

                '
            msg:
                type: string
                description: 'Description of the event specified in action.

                '
            if:
            not:
                properties:
                status:
                    const: error
                action:
                    const: start
            then:
            required:
            - kernel_id
