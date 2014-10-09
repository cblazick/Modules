import os, sys

import unittest
sys.path.append(os.path.abspath(os.path.join(__file__, "../.."))) # jump out one level to import Modules as would happen typically
import Modules.ansi # import Modules indirectly to test __init__ routines

class Modules_testSuite(unittest.TestCase):
    """
    testing routines for the Modules package
    """

    def test_Modules(self):
        self.assertEqual(Modules.globals.TEST, "test")
        self.assertEqual(Modules.globals.AUTHOR, "Chris Blazick")

if __name__ == "__main__":
    unittest.main()
