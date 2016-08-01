"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import abc
from xml.etree.ElementTree import SubElement


class Consumption(metaclass=abc.ABCMeta):
    """
    Class for generating XML messages for elements of type 'ConsumptionType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, name):
        """
        Object constructor.
        """
        self.name = name
        """
        The name of this consumption.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def generate_xml(self, parent):
        """
        Generates the XML element for this consumption.

        :param xml.etree.ElementTree.Element parent: The parent XML element.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml_common(self, parent):
        """
        Generates the common XML elements of the XML element for this consumption.

        :param xml.etree.ElementTree.Element parent: The parent XML element (i.e. the consumption XML element).
        """
        resource_name = SubElement(parent, 'ResourceName')
        resource_name.text = self.name

# ----------------------------------------------------------------------------------------------------------------------
