from xml.etree.ElementTree import SubElement

from lib.enarksh_lib.xml_generator.node.Node import Node


# ----------------------------------------------------------------------------------------------------------------------
class ManualTriggerNode(Node):
    """
    Class for generating XML messages for elements of type 'ManualTriggerType'.
    """

    # -- @todo validate node has no input ports and only one output port.

    # ------------------------------------------------------------------------------------------------------------------
    def generate_xml(self, xml_tree):
        """
        :param xml_tree:
        """
        manual_trigger = SubElement(xml_tree, 'ManualTrigger')

        super().generate_xml(manual_trigger)

# ----------------------------------------------------------------------------------------------------------------------
