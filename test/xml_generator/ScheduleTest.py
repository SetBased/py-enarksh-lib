import os
import unittest

from enarksh_lib.xml_generator.node.CommandJobNode import CommandJobNode
from enarksh_lib.xml_generator.node.ManualTriggerNode import ManualTriggerNode
from enarksh_lib.xml_generator.node.ScheduleNode import ScheduleNode
from enarksh_lib.xml_generator.node.TerminatorNode import TerminatorNode


class ScheduleTest(unittest.TestCase):
    """
    Test cases with complete schedules.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def test01(self):
        """
        Test with very simple schedule.
        """

        # --------------------------------------------------------------------------------------------------------------
        class TestScheduleNode(ScheduleNode):
            # ----------------------------------------------------------------------------------------------------------
            def create_start(self):
                self.username = 'test'

            # ----------------------------------------------------------------------------------------------------------
            def create_child_nodes(self):
                job = ManualTriggerNode('start')
                self.add_child_node(job)

                job = CommandJobNode('ls')
                job.path = '/bin/ls'
                self.add_child_node(job)

                job = TerminatorNode('end')
                self.add_child_node(job)

            # ----------------------------------------------------------------------------------------------------------
            def create_dependencies(self):
                self.add_dependency('ls', '', 'start', '')
                self.add_dependency('end', '', 'ls', '')

        # --------------------------------------------------------------------------------------------------------------
        schedule = TestScheduleNode('TEST01')
        schedule.create_node()
        schedule.finalize()

        with open(os.path.join(os.path.dirname(__file__), 'ScheduleTest', 'test01.xml'), 'rb') as f:
            expected = f.read()

        actual = schedule.get_xml()

        self.assertEqual(expected, actual)

# ----------------------------------------------------------------------------------------------------------------------
