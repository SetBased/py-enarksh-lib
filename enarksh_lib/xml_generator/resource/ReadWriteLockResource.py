from lib.enarksh_lib.xml_generator.resource.Resource import Resource


# ----------------------------------------------------------------------------------------------------------------------
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
