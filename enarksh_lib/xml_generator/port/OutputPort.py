from lib.enarksh_lib.xml_generator.port.Port import Port


# ----------------------------------------------------------------------------------------------------------------------
class OutputPort(Port):
    """
    Class for generating XML messages for elements of type 'OutputPortType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def get_implicit_dependencies_ports(self, ports, level):
        """
        :param list[lib.enarksh_lib.xml_generator.port.Port.Port] ports:
        :param int                                                level:

        :rtype: list[]
        """
        return self._node.get_implicit_dependencies_output_ports(self._port_name, ports, level)

    # ------------------------------------------------------------------------------------------------------------------
    def get_port_type_tag(self):
        """
        :rtype: str
        """
        return 'OutputPort'

# ----------------------------------------------------------------------------------------------------------------------
