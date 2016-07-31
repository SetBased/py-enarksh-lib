"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import abc
from xml.etree.ElementTree import SubElement

from enarksh_lib.xml_generator.node.Node import Node


class CompoundJobNode(Node):
    """
    Class for generating XML messages for elements of type 'CompoundJobType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def create_node(self):
        """
        Execute all the necessary steps the create a compound node.
        """
        self.create_start()
        self.create_resources()
        self.create_child_nodes()
        self.create_input_ports()
        self.create_output_ports()
        self.create_dependencies()
        self.create_finish()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def create_child_nodes(self):
        """
        You MUST override this method in your concrete class to create the child nodes of your compound node.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def create_dependencies(self):
        """
        You MUST override this method in your concrete class to create the dependencies between the child nodes of your
        compound node.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def create_finish(self):
        """
        You MAY override this method in your concrete class to add additional logic for creating your compound node.

        :rtype: None
        """
        # Noting to do.
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def create_input_ports(self):
        """
        You MAY override this method in your concrete class to create additional input ports for your compound node.

        :rtype: None
        """
        # Noting to do.
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def create_output_ports(self):
        """
        You MAY override this method in your concrete class to create additional output ports for your compound node.

        :rtype: None
        """
        # Noting to do.
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def create_resources(self):
        """
        You MAY override this method in your concrete class to create the resources at the level of you compound node.
        node.

        :rtype: None
        """
        # Noting to do.
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def create_start(self):
        """
        You MAY override this method in your concrete class to add additional logic for creating your compound node.

        :rtype: None
        """
        # Noting to do.
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, parent):
        """
        Generates the XML element for this node.

        :param xml.etree.ElementTree.Element parent: The parent XML element.
        """
        compound_job = SubElement(parent, 'CompoundJob')

        self._generate_xml_common(compound_job)

# ----------------------------------------------------------------------------------------------------------------------
