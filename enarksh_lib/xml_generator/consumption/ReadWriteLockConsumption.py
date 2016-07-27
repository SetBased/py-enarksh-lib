from xml.etree.ElementTree import SubElement

from lib.enarksh_lib.xml_generator.consumption.Consumption import Consumption


# ----------------------------------------------------------------------------------------------------------------------
class ReadWriteLockConsumption(Consumption):
    """
    Class ReadWriteLockConsumption
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
        super().generate_xml(xml_tree)

        mode = SubElement(xml_tree, 'Mode')
        mode.text = self._mode

    # ------------------------------------------------------------------------------------------------------------------
    def get_consumption_type_tag(self):
        """
        :rtype: str
        """
        return 'ReadWriteLockConsumption'

# ----------------------------------------------------------------------------------------------------------------------
