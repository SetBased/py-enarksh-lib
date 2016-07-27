"""
Enarksh

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh_lib.xml_generator.node.Node import Node


class ScheduleNode(Node):
    """
    Class for generating XML messages for elements of type 'ScheduleType'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def ensure_dependencies(self):
        for node in self._child_nodes:
            node.ensure_dependencies()

# ----------------------------------------------------------------------------------------------------------------------
