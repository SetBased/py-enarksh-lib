"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from xml.etree.ElementTree import SubElement

from enarksh_lib.xml_generator.resource.Resource import Resource


class ReadWriteLockResource(Resource):
    """
    Class for generating XML messages for elements of type 'ReadWriteLockResourceType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, parent):
        """
        Generates the XML element for this resource.

        :param xml.etree.ElementTree.Element parent: The parent XML element.
        """
        resource = SubElement(parent, 'ReadWriteLockResource')

        self._generate_xml_common(resource)

# ----------------------------------------------------------------------------------------------------------------------
