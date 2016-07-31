"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from xml.etree.ElementTree import SubElement

from enarksh_lib.xml_generator.consumption.Consumption import Consumption


class ReadWriteLockConsumption(Consumption):
    """
    Class for generating XML messages for elements of type 'ReadWriteLockConsumptionType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, name, mode):
        """
        Object constructor.

        :param str name: The name of this consumption.
        :param str mode: The mode of the consumption. Valid values are: 'read' and 'write'.
        """
        Consumption.__init__(self, name)

        self.mode = mode
        """
        The mode of the lock of this consumption.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, parent):
        """
        Generates the XML element for this consumption.

        :param xml.etree.ElementTree.Element parent: The parent XML element.
        """
        consumption = SubElement(parent, 'ReadWriteLockConsumption')

        self.generate_xml_common(consumption)

        mode = SubElement(consumption, 'Mode')
        mode.text = self.mode

# ----------------------------------------------------------------------------------------------------------------------
