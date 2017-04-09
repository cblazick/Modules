import os, sys

import unittest
sys.path.append(os.path.abspath(os.path.join(__file__, "../.."))) # jump out one level to import Modules as would happen typically
import sequence as S

class Modules_testSuite(unittest.TestCase):
    """
    testing routines for the Modules package
    """

    def test_Sequence_frame_list_2_string(self):
        frameList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        unsortedList = [4, 8, 2, 5, 7, 1, 9, 10, 3, 6]

        self.assertEqual(S.frame_list_2_string(frameList), "1-10")
        self.assertEqual(S.frame_list_2_string(unsortedList), "1-10")

        self.assertEqual(S.frame_list_2_string([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]),
                         "-5-5")

        frameList = [2, 4, 6, 8, 10]

        self.assertEqual(S.frame_list_2_string(frameList), "2-10x2")

        frameList = [200, 400, 100, 500, 300]

        self.assertEqual(S.frame_list_2_string(frameList), "100-500x100")

        frameList = [1, 2, 3, 4, 5, 10]

        self.assertEqual(S.frame_list_2_string(frameList), "1-5,10")

        frameList = [1, 2, 3, 4, 5, 8, 10, 12, 14, 20, 21, 23, 26, 30]

        self.assertEqual(S.frame_list_2_string(frameList), "1-5,8-14x2,20,21,23,26,30")

    def test_Sequence_string_2_frame_list(self):

        self.assertEqual(S.string_2_frame_list("1-10"),
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        self.assertEqual(S.string_2_frame_list("100-500x100"),
                         [100, 200, 300, 400, 500])

        self.assertEqual(S.string_2_frame_list("1-5,8-14x2,20,21,23,26,30"),
                         [1, 2, 3, 4, 5, 8, 10, 12, 14, 20, 21, 23, 26, 30])

        self.assertEqual(S.string_2_frame_list("-5-5"),
                         [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])

if __name__ == "__main__":
    unittest.main()
