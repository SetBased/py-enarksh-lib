"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from xml.etree.ElementTree import SubElement

from enarksh_lib.xml_generator.resource.Resource import Resource


class CountingResource(Resource):
    """
    Class for generating XML messages for elements of type 'CountingResourceType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, name, amount):
        """
        Object constructor.
        """
        Resource.__init__(self, name)

        self._amount = amount
        """
        The amount of this resource.

        :type: int
        """

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, xml_tree):
        """
        :param xml_tree:
        """
        Resource.generate_xml(self, xml_tree)

        amount = SubElement(xml_tree, 'Amount')
        amount.text = str(self._amount)

    # ------------------------------------------------------------------------------------------------------------------
    def get_resource_type_tag(self):
        """
        :rtype: str
        """
        return 'CountingResource'

# ----------------------------------------------------------------------------------------------------------------------
