"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh_lib.xml_generator.port.Port import Port


class InputPort(Port):
    """
    Class for generating XML messages for elements of type 'InputPortType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def get_implicit_dependencies_ports(self, ports, level):
        """
        :param list[enarksh_lib.xml_generator.port.Port.Port] ports:
        :param int                                                level:
        """
        self._node.get_implicit_dependencies_input_ports(self._port_name, ports, level)

# ----------------------------------------------------------------------------------------------------------------------
