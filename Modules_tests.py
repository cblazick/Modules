import os, sys

import unittest
sys.path.append(os.path.abspath(".."))
import Modules

class globals_testSuite(unittest.TestCase):
    """
    testing routines for the globals module
    """

    def test_globals(self):
        self.assertEqual(Modules.globals.TEST, "test")
        self.assertEqual(Modules.globals.AUTHOR, "Chris Blazick")

if __name__ == "__main__":
    unittest.main()
