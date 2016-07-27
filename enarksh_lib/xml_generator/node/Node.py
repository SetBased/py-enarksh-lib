from xml.etree.ElementTree import SubElement

from lib.enarksh_lib.xml_generator.port.InputPort import InputPort
from lib.enarksh_lib.xml_generator.port.OutputPort import OutputPort


# ----------------------------------------------------------------------------------------------------------------------
class Node:
    """
    Class for generating XML messages for elements of type 'NodeType'.
    """

    ALL_PORT_NAME = 'all'
    """
    Token for 'all' input or output ports on a node.
    """

    NODE_SELF_NAME = '.'
    """
    Token for node self.
    """

    NODE_ALL_NAME = '*'
    """
    Token for all child nodes.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, name):
        """
        Object constructor.
        """

        self._name = name
        """
        The name of the node.

        :type: str
        """

        self._child_nodes = []
        """
        The child nodes of this node.

        :type: list[]
        """

        self._consumptions = []
        """
        The consumptions.

        :type: list[]
        """

        self._input_ports = []
        """
        The input ports of this node.

        :type: list[]
        """

        self._output_ports = []
        """
        The output ports of this node.

        :type: list[]
        """

        self._parent = None
        """
        The parent node of this node.

        :type: lib.enarksh_lib.xml_generator.node.Node.Node
        """

        self._resources = []
        """
        The resources of this node.

        :type: list[]
        """

        self._username = None
        """
        The user under which this node or its child nodes must run.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def add_child_node(self, child_node):
        """
        Adds a node as a child node of this node.

        :param Node child_node:
        """
        # -- @todo Test node exists.
        # -- @todo Test node is it zelf.
        # -- @todo Test parent node is not set.

        self._child_nodes.append(child_node)
        child_node._parent = self

    # ------------------------------------------------------------------------------------------------------------------
    def add_consumption(self, consumption):
        """
        Adds a consumption as a consumption of this node.

        :param lib.enarksh_lib.xml_generator.node.consumption.Consumption.Consumption consumption:
        """
        # -- @todo test consumption exists.

        self._consumptions.append(consumption)

    # ------------------------------------------------------------------------------------------------------------------
    def add_dependency(self, successor_node_name, successor_port_name, predecessor_node_name, predecessor_port_name):
        """
        :param str successor_node_name:
        :param str successor_port_name:
        :param str predecessor_node_name:
        :param str predecessor_port_name:
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

        for node in self._child_nodes:
            child_port = node.get_input_port(self.ALL_PORT_NAME)
            child_port.add_dependency(parent_port)

    # ------------------------------------------------------------------------------------------------------------------
    def add_dependency_all_output_ports(self):
        """
        Add dependencies between the 'all' output port of this node and the 'all' output of all this child nodes.
        """
        parent_port = self.get_output_port(self.ALL_PORT_NAME)

        for node in self._child_nodes:
            child_port = node.get_output_port(self.ALL_PORT_NAME)
            parent_port.add_dependency(child_port)

    # ------------------------------------------------------------------------------------------------------------------
    def add_resource(self, resource):
        """
        Adds resource 'resource' as a resource of this node.

        :param lib.enarksh_lib.xml_generator.resource.Resource.Resource resource:
        """
        # -- @todo Test resource exists.

        self._resources.append(resource)

    # ------------------------------------------------------------------------------------------------------------------
    def finalize(self):
        """
        Ensures that all required dependencies between the 'all' input and output ports are present and removes
        redundant dependencies between ports and nodes.
        """
        self.ensure_dependencies()
        self.purge()

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, xml_tree):
        """
        Generates XML-code for this node.

        :param xml_tree:
        """
        # Generate XML for the node name.
        node_name = SubElement(xml_tree, 'NodeName')
        node_name.text = self._name

        # Generate XML for username.
        if self._username:
            username = SubElement(xml_tree, 'UserName')
            username.text = self._username

        # Generate XML for input ports.
        if self._input_ports:
            input_ports = SubElement(xml_tree, 'InputPorts')

            for port in self._input_ports:
                port_tree_element = SubElement(input_ports, 'Port')
                port.generate_xml(port_tree_element)

        # Generate XML for resources.
        if self._resources:
            resources = SubElement(xml_tree, 'Resources')

            for resource in self._resources:
                res = SubElement(resources, resource.get_resource_type_tag())
                resource.generate_xml(res)

        # Generate XML for consumptions.
        if self._consumptions:
            consumptions = SubElement(xml_tree, 'Consumptions')

            for consumption in self._consumptions:
                cons = SubElement(consumptions, consumption.get_consumption_type_tag())
                consumption.generate_xml(cons)

        # Generate XML for nodes.
        if self._child_nodes:
            child_nodes = SubElement(xml_tree, 'Nodes')

            for node in self._child_nodes:
                node.pre_generate_xml()
                node.generate_xml(child_nodes)

        # Generate XML for output ports.
        if self._output_ports:
            output_ports = SubElement(xml_tree, 'OutputPorts')

            for port in self._output_ports:
                port_element = SubElement(output_ports, 'Port')
                port.generate_xml(port_element)

    # ------------------------------------------------------------------------------------------------------------------
    def get_child_node(self, name):
        """
        Returns child node with 'name'. If no child node with 'name' exists an exception is thrown.

        :param string name:

        :rtype: None\lib.enarksh_lib.xml_generator.node.Node.Node
        """
        ret = self.search_child_node(name)
        if not ret:
            raise Exception("Child node with name '{0}' doesn't exists".format(name))

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

        :param string name:

        :rtype: None\lib.enarksh_lib.xml_generator.port.Port.Port
        """
        ret = self.search_input_port(name)

        if not ret:
            if name == self.ALL_PORT_NAME:
                ret = self.make_input_port(name)
            else:
                raise Exception("Node '{0}' doesn't have input port '{0}'".format(self._name, name))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def get_input_ports(self):
        """
        Returns all input ports of this node.

        :rtype: list[lib.enarksh_lib.xml_generator.port.InputPort.InputPort]
        """
        return self._input_ports

    # ------------------------------------------------------------------------------------------------------------------
    def get_name(self):
        """
        Returns the name of this node.

        :rtype: str
        """
        return self._name

    # ------------------------------------------------------------------------------------------------------------------
    def get_output_port(self, name):
        """
        Returns output port with 'name'. If no output port with 'name' exists, an exception is thrown.

        :param str name:

        :rtype: lib.enarksh_lib.xml_generator.port.Port.Port
        """
        ret = self.search_output_port(name)

        if not ret:
            if name == self.ALL_PORT_NAME:
                ret = self.make_output_port(name)
            else:
                raise Exception("Node '{0}' doesn't have output port '{1}'".format(self._name, name))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def get_output_ports(self):
        """
        Returns all output ports of this node.

        :rtype: list[lib.enarksh_lib.xml_generator.port.OutputPort.OutputPort
        """
        return self._output_ports

    # ------------------------------------------------------------------------------------------------------------------
    def get_parent(self):
        """
        Returns the parent node of this node.

        :rtype: lib.enarksh_lib.xml_generator.node.Node.Node
        """
        return self._parent

    # ------------------------------------------------------------------------------------------------------------------
    def get_path(self):
        """
        Returns the path of this node.

        :rtype: str
        """
        # -- @todo detect recursion

        path = self._parent.get_path() if self._parent else "/"
        return path + self._name

    # ------------------------------------------------------------------------------------------------------------------
    def get_username(self):
        """
        Returns the username under which this node or its child nodes must run.

        :rtype: str
        """
        return self._username

    # ------------------------------------------------------------------------------------------------------------------
    def make_input_port(self, name):
        """
        Creates an input port with name 'name' and returns that input port.

        :param str name: The name of port.

        :rtype: lib.enarksh_lib.xml_generator.port.Port.Port
        """
        # -- @todo test port already exists.

        port = InputPort(self, name)
        self._input_ports.append(port)

        return port

    # ------------------------------------------------------------------------------------------------------------------
    def make_output_port(self, name):
        """
        Creates an output port with name 'name' and returns that output port.

        :param str name: The name of port.

        :rtype: lib.enarksh_lib.xml_generator.port.Port.Port
        """
        # -- @todo test port already exists.

        port = OutputPort(self, name)
        self._output_ports.append(port)

        return port

    # ------------------------------------------------------------------------------------------------------------------
    def pre_generate_xml(self):
        """
        This function can be called before generation XML and is intended to be overloaded.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def purge(self):
        """
        Removes duplicate dependencies and dependencies that are dependencies of predecessors.
        """
        for port in self._input_ports:
            port.purge()

        for node in self._child_nodes:
            node.purge()

        for port in self._output_ports:
            port.purge()

    # ------------------------------------------------------------------------------------------------------------------
    def remove_child_node(self, node_name):
        """
        Removes node 'node_name' as a child node. The dependencies of any successor of 'node' are been replaced
        with all dependencies of node.

        :param str node_name:
        """
        node = None

        # Find and remove node 'node_name'.
        for tmp in self._child_nodes:
            if tmp.get_name() == node_name:
                node = tmp
                self._child_nodes.remove(tmp)
                break

        if not node:
            raise Exception("Node '{0}' doesn't have child node '{1}'".format(self.get_path(), node_name))

        # Get all dependencies of the node.
        deps = []
        for port in node.get_input_ports():
            for dep in port.get_all_dependencies():
                deps.append(dep)

        for tmp in self._child_nodes:
            tmp.replace_node_dependency(node_name, deps)

        for port in self._output_ports:
            port.replace_node_dependency(node_name, deps)

    # ------------------------------------------------------------------------------------------------------------------
    def replace_node_dependency(self, node_name, dependencies):
        """
        Replaces any dependency of this node on node 'node_name' with dependencies 'dependencies'.

        :param str    node_name:
        :param list[] dependencies:
        """
        for port in self._input_ports:
            port.replace_node_dependency(node_name, dependencies)

    # ------------------------------------------------------------------------------------------------------------------
    def search_child_node(self, name):
        """
        If this node has a child node with name 'name' that child node will be returned.
        If no child node with 'name' exists, returns None.

        :param str name:

        :rtype: None\lib.enarksh_lib.xml_generator.node.Node.Node
        """
        ret = None
        for node in self._child_nodes:
            if node.get_name() == name:
                ret = node
                break

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def search_input_port(self, name):
        """
        If this node has a input port with name 'name' that input port will be returned.
        If no input port with 'name' exists, returns None.

        :param str name:

        :rtype: None\lib.enarksh_lib.xml_generator.port.InputPort.InputPort
        """
        ret = None
        for port in self._input_ports:
            if port.get_name() == name:
                ret = port
                break

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def search_output_port(self, name):
        """
        If this node has a output port with name 'name' that output port will be returned.
        If no output port with 'name' exists, returns None.

        :param str name:

        :rtype: None\lib.enarksh_lib.xml_generator.port.InputPort.InputPort
        """
        ret = None
        for port in self._output_ports:
            if port.get_name() == name:
                ret = port
                break

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def set_name(self, name):
        """
        Sets the name of this node to 'name'.

        :param str name:
        """
        self._name = name

    # ------------------------------------------------------------------------------------------------------------------
    def set_username(self, username):
        """
        Sets the name under which this node or its child nodes must run.

        :param str username:
        """
        # -- @todo Test username not empty of None.

        self._username = username

    # ------------------------------------------------------------------------------------------------------------------
    def ensure_dependencies(self):
        if self._child_nodes:
            input_port_all = self.get_input_port(self.ALL_PORT_NAME)
            # $output_port_all = $this->getOutputPort( self::ALL_PORT_NAME );

            for node in self._child_nodes:
                node.ensure_dependencies()

            # Ensure that output port 'all' depends on all child nodes.
            self.add_dependency_all_output_ports()

            # Ensure input port 'all' of this node depends on output 'all' of each predecessor of this node.
            for input_port in self._input_ports:
                for port in input_port.get_all_dependencies():
                    if port.get_node() != self._parent:
                        input_port_all.add_dependency(port.get_node().get_output_port(self.ALL_PORT_NAME))

# ----------------------------------------------------------------------------------------------------------------------
