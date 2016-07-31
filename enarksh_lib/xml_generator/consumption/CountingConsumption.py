"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from xml.etree.ElementTree import SubElement

from enarksh_lib.xml_generator.consumption.Consumption import Consumption


class CountingConsumption(Consumption):
    """
    Class for generating XML messages for elements of type 'CountingConsumptionType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, name, amount):
        """
        Object constructor.
        """
        Consumption.__init__(self, name)

        self._amount = amount
        """
        The amount consumed by this consumption

        :type: int
        """

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, parent):
        """
        Generates the XML element for this consumption.

        :param xml.etree.ElementTree.Element parent: The parent XML element.
        """
        consumption = SubElement(parent, 'CountingConsumption')

        self.generate_xml_common(consumption)

        amount = SubElement(consumption, 'Amount')
        amount.text = str(self._amount)

# ----------------------------------------------------------------------------------------------------------------------
