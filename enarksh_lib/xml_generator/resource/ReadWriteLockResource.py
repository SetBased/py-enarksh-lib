"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh_lib.xml_generator.resource.Resource import Resource


class ReadWriteLockResource(Resource):
    """
    Class for generating XML messages for elements of type 'ReadWriteLockResourceType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def get_resource_type_tag(self):
        """
        :rtype: str
        """
        return 'ReadWriteLockResource'

# ----------------------------------------------------------------------------------------------------------------------
