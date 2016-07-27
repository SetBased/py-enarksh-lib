"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from xml.etree.ElementTree import SubElement

from enarksh_lib.xml_generator.node.Node import Node


class TerminatorNode(Node):
    """
    Class for generating XML messages for elements of type 'TerminatorType'.
    """

    # -- @todo validate node has only one input port and no output ports.

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, xml_tree):
        """
        :param xml_tree:
        """
        terminator = SubElement(xml_tree, 'Terminator')

        Node.generate_xml(self, terminator)

# ----------------------------------------------------------------------------------------------------------------------
