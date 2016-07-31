"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from xml.etree.ElementTree import SubElement

from enarksh_lib.xml_generator.node.Node import Node


class ManualTriggerNode(Node):
    """
    Class for generating XML messages for elements of type 'ManualTriggerType'.
    """

    # -- @todo validate node has no input ports and only one output port.

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, parent):
        """
        Generates the XML element for this node.

        :param xml.etree.ElementTree.Element parent: The parent XML element.
        """
        manual_trigger = SubElement(parent, 'ManualTrigger')

        self._generate_xml_common(manual_trigger)

# ----------------------------------------------------------------------------------------------------------------------
