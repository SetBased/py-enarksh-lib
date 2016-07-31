"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from xml.etree.ElementTree import SubElement

from enarksh_lib.xml_generator.node.Node import Node


class CommandJobNode(Node):
    """
    Class for generating XML messages for elements of type 'CommandJobType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, name):
        """
        Object constructor.

        :param str name: The name of the node.
        """
        Node.__init__(self, name)

        self.args = []
        """
        The arguments of the executable.

        :type: list[str]
        """

        self.path = ''
        """
        The path of the executable that must be run by this job.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, parent):
        """
        Generates the XML element for this node.

        :param xml.etree.ElementTree.Element parent: The parent XML element.
        """
        command_job = SubElement(parent, 'CommandJob')

        self._generate_xml_common(command_job)

        path = SubElement(command_job, 'Path')
        path.text = self.path

        if self.args:
            args_element = SubElement(command_job, 'Args')

            for arg in self.args:
                argument = SubElement(args_element, 'Arg')
                argument.text = str(arg)

    # ------------------------------------------------------------------------------------------------------------------
    def get_implicit_dependencies_output_ports(self, port_name, ports, level):
        """

        :param str                                                port_name:
        :param list[enarksh_lib.xml_generator.port.Port.Port] ports:
        :param int                                                level:

        :rtype: list[]
        """
        port = self.get_output_port(port_name)

        if port not in ports:
            if level:
                ports.append(port)

        self.get_implicit_dependencies_input_ports(self.ALL_PORT_NAME, ports, level + 1)

# ----------------------------------------------------------------------------------------------------------------------
