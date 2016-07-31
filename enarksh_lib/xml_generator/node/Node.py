"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import abc
from xml.etree.ElementTree import SubElement

from enarksh_lib.xml_generator.port.InputPort import InputPort
from enarksh_lib.xml_generator.port.OutputPort import OutputPort


class Node:
    """
    Class for generating XML messages for elements of type 'NodeType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    ALL_PORT_NAME = 'all'
    """
    Token for 'all' input or output ports on a node.

    :type: str
    """

    NODE_SELF_NAME = '.'
    """
    Token for node self.

    :type: str
    """

    NODE_ALL_NAME = '*'
    """
    Token for all child nodes.

    :type: str
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, name):
        """
        Object constructor.

        :param str name: The name of the node.
        """
        self.name = name
        """
        The name of the node.

        :type: str
        """

        self.child_nodes = []
        """
        The child nodes of this node.

        :type: list[enarksh_lib.xml_generator.node.Node.Node]
        """

        self.consumptions = []
        """
        The consumptions.

        :type: list[enarksh_lib.xml_generator.consumption.Consumption.Consumption]
        """

        self.input_ports = []
        """
        The input ports of this node.

        :type: list[enarksh_lib.xml_generator.port.InputPort.InputPort]
        """

        self.output_ports = []
        """
        The output ports of this node.

        :type: list[enarksh_lib.xml_generator.port.OutputPort.OutputPort]
        """

        self.parent = None
        """
        The parent node of this node.

        :type: enarksh_lib.xml_generator.node.Node.Node
        """

        self.resources = []
        """
        The resources of this node.

        :type: list[enarksh_lib.xml_generator.resource.Resource.Resource]
        """

        self.username = ''
        """
        The user under which this node or its child nodes must run.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def add_child_node(self, child_node):
        """
        Adds a node as a child node of this node.

        :param enarksh_lib.xml_generator.node.Node.Node child_node: The new child node.
        """
        # -- @todo Test node exists.
        # -- @todo Test node is not self.
        # -- @todo Test parent node is not set.

        self.child_nodes.append(child_node)
        child_node.parent = self

    # ------------------------------------------------------------------------------------------------------------------
    def add_dependency(self, successor_node_name, successor_port_name, predecessor_node_name, predecessor_port_name):
        """
        Adds a dependency between two child nodes are this node and a child node.

        :param str successor_node_name: The successor node (use NODE_SELF_NAME for the this node).
        :param str successor_port_name: The successor port.
        :param str predecessor_node_name: The predecessor node (use NODE_SELF_NAME for the this node).
        :param str predecessor_port_name: The predecessor port.
        """
        if not predecessor_port_name:
            predecessor_port_name = self.ALL_PORT_NAME
        if not successor_port_name:
            successor_port_name = self.ALL_PORT_NAME

        if successor_node_name == self.NODE_SELF_NAME:
            succ_port = self.get_output_port(successor_port_name)
        else:
            succ_node = self.get_child_node(successor_node_name)
            succ_port = succ_node.get_input_port(successor_port_name)

        if predecessor_node_name == '.':
            pred_port = self.get_input_port(predecessor_port_name)
        else:
            pred_node = self.get_child_node(predecessor_node_name)
            pred_port = pred_node.get_output_port(predecessor_port_name)

        succ_port.add_dependency(pred_port)

    # ------------------------------------------------------------------------------------------------------------------
    def add_dependency_all_input_ports(self):
        """
        Add dependencies between the 'all' input port of this node and the 'all' input port of all this child nodes.
        """
        parent_port = self.get_input_port(self.ALL_PORT_NAME)

        for node in self.child_nodes:
            child_port = node.get_input_port(self.ALL_PORT_NAME)
            child_port.add_dependency(parent_port)

    # ------------------------------------------------------------------------------------------------------------------
    def add_dependency_all_output_ports(self):
        """
        Add dependencies between the 'all' output port of this node and the 'all' output of all this child nodes.
        """
        parent_port = self.get_output_port(self.ALL_PORT_NAME)

        for node in self.child_nodes:
            child_port = node.get_output_port(self.ALL_PORT_NAME)
            parent_port.add_dependency(child_port)

    # ------------------------------------------------------------------------------------------------------------------
    def finalize(self):
        """
        Ensures that all required dependencies between the 'all' input and output ports are present and removes
        redundant dependencies between ports and nodes.
        """
        self.ensure_dependencies()
        self.purge()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def generate_xml(self, parent):
        """
        Generates the XML element for this node.

        :param xml.etree.ElementTree.Element parent: The parent XML element.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _generate_xml_common(self, parent):
        """
        Generates the common XML elements of the XML element for this  node.

        :param xml.etree.ElementTree.Element parent: The parent XML element (i.e. the node XML element).
        """
        # Generate XML for the node name.
        node_name = SubElement(parent, 'NodeName')
        node_name.text = self.name

        # Generate XML for username.
        if self.username:
            username = SubElement(parent, 'UserName')
            username.text = self.username

        # Generate XML for input ports.
        if self.input_ports:
            input_ports = SubElement(parent, 'InputPorts')
            for port in self.input_ports:
                port.generate_xml(input_ports)

        # Generate XML for resources.
        if self.resources:
            resources = SubElement(parent, 'Resources')
            for resource in self.resources:
                resource.generate_xml(resources)

        # Generate XML for consumptions.
        if self.consumptions:
            consumptions = SubElement(parent, 'Consumptions')
            for consumption in self.consumptions:
                consumption.generate_xml(consumptions)

        # Generate XML for nodes.
        if self.child_nodes:
            child_nodes = SubElement(parent, 'Nodes')
            for node in self.child_nodes:
                node.pre_generate_xml()
                node.generate_xml(child_nodes)

        # Generate XML for output ports.
        if self.output_ports:
            output_ports = SubElement(parent, 'OutputPorts')
            for port in self.output_ports:
                port.generate_xml(output_ports)

    # ------------------------------------------------------------------------------------------------------------------
    def get_child_node(self, name):
        """
        Returns a child node by name. If no child node such name exists an exception is thrown.

        :param str name: The name of the child node.

        :rtype: enarksh_lib.xml_generator.node.Node.Node
        """
        ret = self.search_child_node(name)
        if not ret:
            raise ValueError("Child node with name '{0}' doesn't exists".format(name))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def get_implicit_dependencies_input_ports(self, port_name, ports, level):
        """
        :param string port_name:
        :param list[] ports:
        :param int    level:
        """
        port = self.get_input_port(port_name)

        if port not in ports:
            if level:
                ports.append(port)
            port.get_dependencies_ports(ports, level + 1)

    # ------------------------------------------------------------------------------------------------------------------
    def get_implicit_dependencies_output_ports(self, port_name, ports, level):
        """
        :param string port_name:
        :param list[] ports:
        :param int    level:
        """
        port = self.get_output_port(port_name)

        if port not in ports:
            if level:
                ports.append(port)
            port.get_dependencies_ports(ports, level + 1)

    # ------------------------------------------------------------------------------------------------------------------
    def get_input_port(self, name):
        """
        Returns input port with 'name'. If no input port with 'name' exists an exception is thrown.

        :param string name: The name of the port.

        :rtype: enarksh_lib.xml_generator.port.Port.Port
        """
        ret = self.search_input_port(name)

        if not ret:
            if name == self.ALL_PORT_NAME:
                ret = self.make_input_port(name)
            else:
                raise Exception("Node '{0}' doesn't have input port '{1}'".format(self.name, name))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def get_output_port(self, name):
        """
        Returns output port with 'name'. If no output port with 'name' exists, an exception is thrown.

        :param str name: The name of the output port.

        :rtype: enarksh_lib.xml_generator.port.Port.Port
        """
        ret = self.search_output_port(name)

        if not ret:
            if name == self.ALL_PORT_NAME:
                ret = self.make_output_port(name)
            else:
                raise Exception("Node '{0}' doesn't have output port '{1}'".format(self.name, name))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def get_path(self):
        """
        Returns the path of this node.

        :rtype: str
        """
        # -- @todo detect recursion
        path = self.parent.get_path() if self.parent else "/"

        return path + self.name

    # ------------------------------------------------------------------------------------------------------------------
    def make_input_port(self, name):
        """
        Creates an input port with name 'name' and returns that input port.

        :param str name: The name of port.

        :rtype: enarksh_lib.xml_generator.port.Port.Port
        """
        # -- @todo test port already exists.

        port = InputPort(self, name)
        self.input_ports.append(port)

        return port

    # ------------------------------------------------------------------------------------------------------------------
    def make_output_port(self, name):
        """
        Creates an output port with name 'name' and returns that output port.

        :param str name: The name of port.

        :rtype: enarksh_lib.xml_generator.port.Port.Port
        """
        # -- @todo test port already exists.

        port = OutputPort(self, name)
        self.output_ports.append(port)

        return port

    # ------------------------------------------------------------------------------------------------------------------
    def pre_generate_xml(self):
        """
        This function can be called before generation XML and is intended to be overloaded.

        :rtype: None
        """
        # Nothing to do.
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def purge(self):
        """
        Removes duplicate dependencies and dependencies that are dependencies of predecessors.
        """
        for port in self.input_ports:
            port.purge()

        for node in self.child_nodes:
            node.purge()

        for port in self.output_ports:
            port.purge()

    # ------------------------------------------------------------------------------------------------------------------
    def remove_child_node(self, node_name):
        """
        Removes node 'node_name' as a child node. The dependencies of any successor of 'node' will be replaced
        with all dependencies of the removed node.

        :param str node_name:
        """
        node = None

        # Find and remove node 'node_name'.
        for tmp in self.child_nodes:
            if tmp.name == node_name:
                node = tmp
                self.child_nodes.remove(tmp)
                break

        if not node:
            raise Exception("Node '{0}' doesn't have child node '{1}'".format(self.get_path(), node_name))

        # Get all dependencies of the node.
        deps = []
        for port in node.input_ports:
            for dep in port.get_all_dependencies():
                deps.append(dep)

        for tmp in self.child_nodes:
            tmp.replace_node_dependency(node_name, deps)

        for port in self.output_ports:
            port.replace_node_dependency(node_name, deps)

    # ------------------------------------------------------------------------------------------------------------------
    def replace_node_dependency(self, node_name, dependencies):
        """
        Replaces any dependency of this node on node 'node_name' with dependencies 'dependencies'.

        :param str    node_name:
        :param list[] dependencies:
        """
        for port in self.input_ports:
            port.replace_node_dependency(node_name, dependencies)

    # ------------------------------------------------------------------------------------------------------------------
    def search_child_node(self, name):
        """
        If this node has a child node with name 'name' that child node will be returned.
        If no child node with 'name' exists, returns None.

        :param str name: The name of the child node.

        :rtype: None|enarksh_lib.xml_generator.node.Node.Node
        """
        ret = None
        for node in self.child_nodes:
            if node.name == name:
                ret = node
                break

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def search_input_port(self, name):
        """
        If this node has a input port with name 'name' that input port will be returned.
        If no input port with 'name' exists, returns None.

        :param str name: The name of the input port.

        :rtype: None|enarksh_lib.xml_generator.port.InputPort.InputPort
        """
        ret = None
        for port in self.input_ports:
            if port.port_name == name:
                ret = port
                break

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def search_output_port(self, name):
        """
        If this node has a output port with name 'name' that output port will be returned.
        If no output port with 'name' exists, returns None.

        :param str name: The name of the output port.

        :rtype: None|enarksh_lib.xml_generator.port.InputPort.InputPort
        """
        ret = None
        for port in self.output_ports:
            if port.port_name == name:
                ret = port
                break

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def ensure_dependencies(self):
        """
        Creates the following dependencies:
        - Dependencies between the input port 'all' and the input port 'all' of all the child nodes of this nodes.
        - Dependencies between all output ports 'all' of all child nodes and the output port 'all' of this node.
        - Dependencies between the input port 'all' of this node and the output ports 'all' of all predecessor nodes of
          this node.
        This is done recursively for all child node.

        Remember: Redundant and duplicate dependencies are removed by purge().
        """
        if self.child_nodes:
            # Apply this method recursively for all child node.
            for node in self.child_nodes:
                node.ensure_dependencies()

            # Ensure that the input port 'all' of all child nodes depends on input port 'all' of this node.
            self.add_dependency_all_input_ports()

            # Ensure that output port 'all' of the node depends on all output ports 'all' of all child nodes.
            self.add_dependency_all_output_ports()

            # Ensure input port 'all' of this node depends on output 'all' of each predecessor of this node.
            input_port_all = self.get_input_port(self.ALL_PORT_NAME)
            for input_port in self.input_ports:
                for port in input_port.get_all_dependencies():
                    if port.node != self.parent:
                        input_port_all.add_dependency(port.node.get_output_port(self.ALL_PORT_NAME))

# ----------------------------------------------------------------------------------------------------------------------
