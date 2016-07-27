"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from xml.etree.ElementTree import SubElement

from enarksh_lib.xml_generator.node.Node import Node


class CompoundJobNode(Node):
    """
    Class for generating XML messages for elements of type 'CompoundJobType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, xml_tree):
        """
        :param xml_tree:
        """
        compound_job = SubElement(xml_tree, 'CompoundJob')

        super().generate_xml(compound_job)

# ----------------------------------------------------------------------------------------------------------------------
