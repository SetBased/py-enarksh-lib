"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import abc
from xml.etree.ElementTree import SubElement


class Port:
    """
    Class Port
    Class for generating XML messages for elements of type 'InputPortType' and 'OutputPortType'.
    """

    NODE_SELF_NAME = '.'  # -- @todo Discuss about this constant, because I can't import Node.
    """
    Token for node self.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, node, port_name):
        """
        Object constructor.
        """

        self.node = node
        """
        The node of which this port is a port.

        :type: enarksh_lib.xml_generator.node.Node.Node
        """

        self.port_name = port_name
        """
        The name of this port.

        :type: str
        """

        self._predecessors = []
        """
        The dependencies of this port.

        :type: list[enarksh_lib.xml_generator.port.Port.Port]
        """

        self._successors = []
        """
        The dependants of this port.

        :type: list[enarksh_lib.xml_generator.port.Port.Port]
        """

    # ------------------------------------------------------------------------------------------------------------------
    def add_dependency(self, port):
        """
        Add a port as a dependency of this port.

        :param enarksh_lib.xml_generator.port.Port.Port port: The port that depends on this port.
        """
        # -- @todo Validate owner of port and owner of this port.

        if port not in self._predecessors:
            self._predecessors.append(port)

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, parent):
        """
        Generates the XML element for this port.

        :param xml.etree.ElementTree.Element parent: The parent XML element.
        """
        port = SubElement(parent, 'Port')

        port_name = SubElement(port, 'PortName')
        port_name.text = self.port_name

        if self._predecessors:
            dependencies_element = SubElement(port, 'Dependencies')

            for predecessor in self._predecessors:
                dependency = SubElement(dependencies_element, 'Dependency')

                node_name = SubElement(dependency, 'NodeName')
                if predecessor.node == self.node.parent:
                    node_name.text = self.NODE_SELF_NAME
                else:
                    node_name.text = predecessor.node.name

                port_name = SubElement(dependency, 'PortName')
                port_name.text = self.port_name

    # ------------------------------------------------------------------------------------------------------------------
    def get_all_dependencies(self):
        """
        Returns all the dependencies of this port.

        :rtype: enarksh_lib.xml_generator.port.Port.Port port:
        """
        return self._predecessors

    # ------------------------------------------------------------------------------------------------------------------
    def get_dependencies_ports(self, ports, level):
        """

        :param list[enarksh_lib.xml_generator.port.Port.Port] ports:
        :param int                                            level:

        :rtype: list[]
        """
        for port in self._predecessors:
            if port not in ports:
                if level:
                    ports.append(port)
                port.get_implicit_dependencies_ports(ports, level + 1)

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_implicit_dependencies_ports(self, ports, level):
        """
        :param list[enarksh_lib.xml_generator.port.Port.Port] ports:
        :param int                                            level:
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def purge(self):
        """
        Removes dependencies from this port that are implicit dependencies (via one or more predecessors).
        """
        # Get all implicit dependencies ports.
        implicit_dependencies = []
        for port in self._predecessors:
            port.get_implicit_dependencies_ports(implicit_dependencies, 0)

        # Create a new dependency array without implicit dependencies.
        direct_dependencies = []
        for port in self._predecessors:
            if port not in implicit_dependencies:

                # Prevent duplicate dependencies.
                if port not in direct_dependencies:
                    direct_dependencies.append(port)

        self._predecessors = direct_dependencies

    # ------------------------------------------------------------------------------------------------------------------
    def replace_node_dependency(self, node_name, dependencies):
        """
        Replaces any dependency of this port on node 'node_name' with dependencies 'dependencies'.

        :param str    node_name:
        :param list[] dependencies:
        """
        obsolete = []

        # Find any predecessor that depends on node 'node_name'.
        for index, port in enumerate(self._predecessors):
            if port.node.name == node_name:
                obsolete.append(index)

        if obsolete:
            # Remove all dependencies of node 'node_name'.
            for index in obsolete:
                self._predecessors.pop(index)

            # And replace those dependencies with 'dependencies'.
            for dep in dependencies:
                self._predecessors.append(dep)

# ----------------------------------------------------------------------------------------------------------------------
