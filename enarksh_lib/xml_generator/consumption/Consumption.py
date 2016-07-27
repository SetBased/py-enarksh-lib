import abc
from xml.etree.ElementTree import SubElement


# ----------------------------------------------------------------------------------------------------------------------
class Consumption:
    """
    Class for generating XML messages for elements of type 'ConsumptionType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, name):
        """
        Object constructor.
        """

        self._name = name
        """
        The name of this consumption.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, xml_tree):
        """
        Generates XML-code for this consumption.

        :param xml_tree:
        """
        resource_name = SubElement(xml_tree, 'ResourceName')
        resource_name.text = self._name

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_consumption_type_tag(self):
        """
        Returns the XML-tag for the type of this consumption.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
