import unittest
from stdin_stdout_redirect import captured_io
from user_interface import user_interface
import unittest
from unittest.mock import patch
import sys
from io import StringIO
from stdin_stdout_redirect import captured_output

class TestUserInterface(unittest.TestCase):
    
    def test_exit_system(self):
        """
        This function is used to test that the eit_system() function exits out 
        of the system andprints out the exit message.
        """

        with captured_output() as (stdoutobject, stderrobject):
            user_interface.exit_system()
        output = stdoutobject.getvalue().strip()
        self.assertEqual(output, "You have logged out of the WeThinkCode Code Clinic Booking System.",)
