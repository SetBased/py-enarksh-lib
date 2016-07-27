import abc
from xml.etree.ElementTree import SubElement


# ----------------------------------------------------------------------------------------------------------------------
class Resource:
    """
    Class for generating XML messages for elements of type 'ResourceType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, name):
        """
        Object constructor.
        """

        self._name = name
        """
        The name of this resource.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, xml_tree):
        """
        Generates XML-code for this resource.

        :param xml_tree:
        """
        resource_name = SubElement(xml_tree, 'ResourceName')
        resource_name.text = self._name

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_resource_type_tag(self):
        """
        Returns the XML-tag for the type of this resource.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
