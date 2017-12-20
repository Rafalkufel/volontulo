"""
.. module:: test_popdb_command
"""

from io import StringIO
from django.core.management import call_command
from django.test import TestCase


class PopdbTest(TestCase):
    """Test for popdb command."""

    def test_command_output(self):
        """Testing if popdb command get proper output"""
        out = StringIO()
        call_command('popdb', stdout=out)
        self.assertIn('Database successfully populated', out.getvalue())
