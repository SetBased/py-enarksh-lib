from xml.etree.ElementTree import SubElement

from lib.enarksh_lib.xml_generator.consumption.Consumption import Consumption


# ----------------------------------------------------------------------------------------------------------------------
class CountingConsumption(Consumption):
    """
    Class CountingConsumption
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
    def generate_xml(self, xml_tree):
        """
        :param xml_tree:
        """
        super().generate_xml(xml_tree)

        amount = SubElement(xml_tree, 'Amount')
        amount.text = str(self._amount)

    # ------------------------------------------------------------------------------------------------------------------
    def get_consumption_type_tag(self):
        """
        :rtype: str
        """
        return 'CountingConsumption'

# ----------------------------------------------------------------------------------------------------------------------
