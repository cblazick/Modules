import os, sys

import unittest
import globals
globals.run()

class globals_testSuite(unittest.TestCase):
    """
    testing routines for the globals module
    """

    def test_globals(self):
        self.assertEqual(globals.TEST, "test")
        self.assertEqual(globals.AUTHOR, "Chris Blazick")

if __name__ == "__main__":
    unittest.main()
