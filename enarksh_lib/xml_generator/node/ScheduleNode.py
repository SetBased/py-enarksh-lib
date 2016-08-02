"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import abc
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement

from enarksh_lib.xml_generator.node.CompoundJobNode import CompoundJobNode


class ScheduleNode(CompoundJobNode, metaclass=abc.ABCMeta):
    """
    Class for generating XML messages for elements of type 'ScheduleType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def get_xml(self, encoding='utf-8'):
        """
        Returns the XML-code of this schedule.

        The returned byte string contains the XML in the requested encoding. You save the byte sting to file in binary
        mode (the file will encoded the requested encoding). Or you can convert the byte string to a string with
        .decode(encoding).

        :param str encoding: The encoding of the XML.

        :rtype: bytes
        """
        tree = Element(None)
        self.generate_xml(tree)

        xml_string = ElementTree.tostring(tree)
        document = minidom.parseString(xml_string)

        return document.toprettyxml(indent=' ', encoding=encoding)

    # ------------------------------------------------------------------------------------------------------------------
    def ensure_dependencies(self):
        """
        Remember a schedule node is the only compound node without input and output ports. Therefore we must override
        this method.
        """
        # Apply this method recursively for all child node.
        for node in self.child_nodes:
            node.ensure_dependencies()

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, parent):
        """
        Generates the XML element for this node.
        """
        schedule = SubElement(parent, 'Schedule')

        self._generate_xml_common(schedule)

# ----------------------------------------------------------------------------------------------------------------------
