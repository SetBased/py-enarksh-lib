import os
import unittest

from enarksh_lib.xml_generator.node.CommandJobNode import CommandJobNode
from enarksh_lib.xml_generator.node.CompoundJobNode import CompoundJobNode
from enarksh_lib.xml_generator.node.ManualTriggerNode import ManualTriggerNode
from enarksh_lib.xml_generator.node.Node import Node
from enarksh_lib.xml_generator.node.ScheduleNode import ScheduleNode
from enarksh_lib.xml_generator.node.TerminatorNode import TerminatorNode
from enarksh_lib.xml_generator.port.InputPort import InputPort
from enarksh_lib.xml_generator.port.OutputPort import OutputPort


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

    # ------------------------------------------------------------------------------------------------------------------
    def test02(self):
        """
        Test with simple schedule with a compound node.
        """

        # --------------------------------------------------------------------------------------------------------------
        class TestSpamAndEggsNode(CompoundJobNode):
            # ----------------------------------------------------------------------------------------------------------
            def make_job_spam(self):
                job = CommandJobNode('spam')
                job.path = '/bin/ls'
                job.args.append('spam')
                self.add_child_node(job)

            # ----------------------------------------------------------------------------------------------------------
            def make_job_eggs(self):
                job = CommandJobNode('eggs')
                job.path = '/bin/ls'
                job.args.append('eggs')
                self.add_child_node(job)

            # ----------------------------------------------------------------------------------------------------------
            def create_child_nodes(self):
                self.make_job_spam()
                self.make_job_eggs()

            # ----------------------------------------------------------------------------------------------------------
            def create_dependencies(self):
                # Nothing to do. Jobs spam and eggs can run in parallel.
                pass

        # --------------------------------------------------------------------------------------------------------------
        class TestScheduleNode(ScheduleNode):
            # ----------------------------------------------------------------------------------------------------------
            def create_start(self):
                self.username = 'test'

            # ----------------------------------------------------------------------------------------------------------
            def make_job_start(self):
                job = ManualTriggerNode('start')
                self.add_child_node(job)

            # ----------------------------------------------------------------------------------------------------------
            def make_job_spam_and_eggs(self):
                job = TestSpamAndEggsNode('spam_and_eggs')
                job.create_node()
                self.add_child_node(job)

            # ----------------------------------------------------------------------------------------------------------
            def make_job_end(self):
                job = TerminatorNode('end')
                self.add_child_node(job)

            # ----------------------------------------------------------------------------------------------------------
            def create_child_nodes(self):
                self.make_job_start()
                self.make_job_spam_and_eggs()
                self.make_job_end()

            # ----------------------------------------------------------------------------------------------------------
            def create_dependencies(self):
                self.add_dependency('spam_and_eggs', '', 'start', '')
                self.add_dependency('end', '', 'spam_and_eggs', '')

        # --------------------------------------------------------------------------------------------------------------
        schedule = TestScheduleNode('TEST02')
        schedule.create_node()
        schedule.finalize()

        with open(os.path.join(os.path.dirname(__file__), 'ScheduleTest', 'test02.xml'), 'rb') as f:
            expected = f.read()

        actual = schedule.get_xml()

        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test03(self):
        """
        Test with simple schedule with two compound nodes and additional input and output ports.
        """

        # --------------------------------------------------------------------------------------------------------------
        class TestSpamAndFooNode(CompoundJobNode):
            # ----------------------------------------------------------------------------------------------------------
            def make_job_spam(self):
                job = CommandJobNode('spam')
                job.path = '/bin/ls'
                job.args.append('spam')
                self.add_child_node(job)

            # ----------------------------------------------------------------------------------------------------------
            def make_job_foo(self):
                job = CommandJobNode('foo')
                job.path = '/bin/ls'
                job.args.append('foo')
                self.add_child_node(job)

            # ----------------------------------------------------------------------------------------------------------
            def create_output_ports(self):
                port = OutputPort(self, 'spam')
                self.output_ports.append(port)

                port = OutputPort(self, 'foo')
                self.output_ports.append(port)

            # ----------------------------------------------------------------------------------------------------------
            def create_child_nodes(self):
                self.make_job_spam()
                self.make_job_foo()

            # ----------------------------------------------------------------------------------------------------------
            def create_dependencies(self):
                # Jobs spam and foo can run in parallel.
                self.add_dependency('.', 'spam', 'spam', '')
                self.add_dependency('.', 'foo', 'foo', '')

        # --------------------------------------------------------------------------------------------------------------
        class TestEggsAndBarNode(CompoundJobNode):
            # ----------------------------------------------------------------------------------------------------------
            def make_job_eggs(self):
                job = CommandJobNode('eggs')
                job.path = '/bin/ls'
                job.args.append('eggs')
                self.add_child_node(job)

            # ----------------------------------------------------------------------------------------------------------
            def make_job_bar(self):
                job = CommandJobNode('bar')
                job.path = '/bin/ls'
                job.args.append('bar')
                self.add_child_node(job)

            # ----------------------------------------------------------------------------------------------------------
            def create_input_ports(self):
                port = InputPort(self, 'eggs')
                self.input_ports.append(port)

                port = InputPort(self, 'bar')
                self.input_ports.append(port)

            # ----------------------------------------------------------------------------------------------------------
            def create_child_nodes(self):
                self.make_job_eggs()
                self.make_job_bar()

            # ----------------------------------------------------------------------------------------------------------
            def create_dependencies(self):
                # Jobs eggs and bar can run in parallel.
                self.add_dependency('eggs', '', '.', 'eggs')
                self.add_dependency('bar', '', '.', 'bar')

            # ----------------------------------------------------------------------------------------------------------
            def ensure_dependencies_input_port(self):
                # Nothing to do.
                pass

        # --------------------------------------------------------------------------------------------------------------
        class TestScheduleNode(ScheduleNode):
            # ----------------------------------------------------------------------------------------------------------
            def create_start(self):
                self.username = 'test'

            # ----------------------------------------------------------------------------------------------------------
            def make_job_start(self):
                job = ManualTriggerNode('start')
                self.add_child_node(job)

            # ----------------------------------------------------------------------------------------------------------
            def make_job_spam_and_foo(self):
                job = TestSpamAndFooNode('spam_and_foo')
                job.create_node()
                self.add_child_node(job)

            # ----------------------------------------------------------------------------------------------------------
            def make_job_eggs_and_bar(self):
                job = TestEggsAndBarNode('eggs_and_bar')
                job.create_node()
                self.add_child_node(job)

            # ----------------------------------------------------------------------------------------------------------
            def make_job_end(self):
                job = TerminatorNode('end')
                self.add_child_node(job)

            # ----------------------------------------------------------------------------------------------------------
            def create_child_nodes(self):
                self.make_job_start()
                self.make_job_spam_and_foo()
                self.make_job_eggs_and_bar()
                self.make_job_end()

            # ----------------------------------------------------------------------------------------------------------
            def create_dependencies(self):
                self.add_dependency('spam_and_foo', '', 'start', '')
                self.add_dependency('eggs_and_bar', 'eggs', 'spam_and_foo', 'spam')
                self.add_dependency('eggs_and_bar', 'bar', 'spam_and_foo', 'foo')
                self.add_dependency('end', '', 'eggs_and_bar', '')

        # --------------------------------------------------------------------------------------------------------------
        schedule = TestScheduleNode('TEST03')
        schedule.create_node()
        schedule.finalize()

        with open(os.path.join(os.path.dirname(__file__), 'ScheduleTest', 'test03.xml'), 'rb') as f:
            expected = f.read()

        actual = schedule.get_xml()

        self.assertEqual(expected, actual)

# ----------------------------------------------------------------------------------------------------------------------
