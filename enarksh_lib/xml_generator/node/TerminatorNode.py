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
    def generate_xml(self, parent):
        """
        Generates the XML element for this node.

        :param xml.etree.ElementTree.Element parent: The parent XML element.
        """
        terminator = SubElement(parent, 'Terminator')

        self._generate_xml_common(terminator)

# ----------------------------------------------------------------------------------------------------------------------
