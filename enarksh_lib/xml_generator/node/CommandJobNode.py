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
        Node.__init__(self, name)

        self.args = []
        """
        The arguments of the executable.

        :type: list[]
        """

        self.path = ''
        """
        The path of the executable that must be run by this job.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, xml_tree):
        """
        :param xml_tree:
        """
        command_job = SubElement(xml_tree, 'CommandJob')

        super().generate_xml(command_job)

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

    # ------------------------------------------------------------------------------------------------------------------
    def set_argument(self, argument):
        """
        Adds 'argument' to the argument list.

        :param str argument:
        """
        self.args.append(argument)

    # ------------------------------------------------------------------------------------------------------------------
    def set_command(self, command):
        """
        Set the path and the arguments based on 'command'. Use this function only when there are no spaces in the
        path or in any argument.

        :param str command:
        """
        # -- @todo IMPLEMENT THIS METHOD
        raise NotImplementedError("LOOK IN ORIGINAL IMPLEMENT METHOD")

    # ------------------------------------------------------------------------------------------------------------------
    def set_path(self, path):
        """
        Set the path to the executable that must be run by this job.

        :param str path: The path to the executable that must be run by this job
        """
        self.path = path

# ----------------------------------------------------------------------------------------------------------------------
