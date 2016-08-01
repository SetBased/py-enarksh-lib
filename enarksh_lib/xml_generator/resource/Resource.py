"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import abc
from xml.etree.ElementTree import SubElement


class Resource(metaclass=abc.ABCMeta):
    """
    Class for generating XML messages for elements of type 'ResourceType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, name):
        """
        Object constructor.

        :param str name: The name of this resource.
        """
        self.name = name
        """
        The name of this resource.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def generate_xml(self, parent):
        """
        Generates the XML element for this resource.

        :param xml.etree.ElementTree.Element parent: The parent XML element.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _generate_xml_common(self, parent):
        """
        Generates the common XML elements of the XML element for this

        :param xml.etree.ElementTree.Element parent: The parent XML element (i.e. the resource XML element).
        """
        resource_name = SubElement(parent, 'ResourceName')
        resource_name.text = self.name

# ----------------------------------------------------------------------------------------------------------------------
