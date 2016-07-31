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

        :param str name: The name of this resource.
        :param int amount: The amount of this resource.
        """
        Resource.__init__(self, name)

        self.amount = amount
        """
        The amount of this resource.

        :type: int
        """

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, parent):
        """
        Generates the XML element for this resource.

        :param xml.etree.ElementTree.Element parent: The parent XML element.
        """
        resource = SubElement(parent, 'CountingResource')

        self._generate_xml_common(resource)

        amount = SubElement(resource, 'Amount')
        amount.text = str(self.amount)

# ----------------------------------------------------------------------------------------------------------------------
