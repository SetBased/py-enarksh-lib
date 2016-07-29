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
        """
        Consumption.__init__(self, name)

        self._mode = mode
        """
        The mode of the lock of this consumption.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, xml_tree):
        """
        :param xml_tree:
        """
        Consumption.generate_xml(self, xml_tree)

        mode = SubElement(xml_tree, 'Mode')
        mode.text = self._mode

    # ------------------------------------------------------------------------------------------------------------------
    def get_consumption_type_tag(self):
        """
        :rtype: str
        """
        return 'ReadWriteLockConsumption'

# ----------------------------------------------------------------------------------------------------------------------
