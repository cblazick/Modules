import os, sys

import unittest
sys.path.append(os.path.abspath(os.path.join(__file__, "../.."))) # jump out one level to import Modules as would happen typically
import sequence as S


class Modules_test_sequence_class(unittest.TestCase):
    """
    testing routines for the Modules package
    """

    def setUp(self):
        self.testdir = "./test_dir"
        self.testdir = os.path.abspath(self.testdir)

        for i in range(1, 15 + 1):
            f = open(os.path.join(self.testdir, "image_file.%05d.jpg" % (i)), "w")
            f.close()


    def runTest(self):
        self.assertRaises(S.SequenceFormatException,
                          S.sequence,
                          "")

        self.assertRaises(S.SequenceFormatException,
                          S.sequence,
                          ["one", "two"])

        s = S.sequence("/directory/file.1-10#.exr")

        self.assertEqual(s.directory, "/directory")
        self.assertEqual(s.padding, 4)
        self.assertEqual(s.isSingleFile(), False)
        self.assertEqual(s.frames, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(s.prefix, "file")
        self.assertEqual(s.lsep, ".")
        self.assertEqual(s.rsep, ".")
        self.assertEqual(s.ext, "exr")
        self.assertEqual(s.isContiguous(), True)

        s = S.sequence("/directory/file.1-10,13-20.exr")

        self.assertEqual(s.isContiguous(), False)
        self.assertEqual(s.padding, 2)

        s = S.sequence("/directory/file.*.exr")

        self.assertEqual(s.padding, None)
        self.assertEqual(s.frames, [])

        path = os.path.join(self.testdir, "image_file.*.jpg")
        s = S.sequence(path)

        self.assertEqual(s.padding, 5)
        self.assertEqual(s.frames, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

        self.assertEqual(s.isContiguous(), True)
        # NEEDED: filesExist test

    def tearDown(self):
        for i in range(1, 15 + 1):
            os.unlink(os.path.join(self.testdir, "image_file.%05d.jpg" % (i)))


class Modules_test_sequence_frame_list_2_strin(unittest.TestCase):

    def runTest(self):
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

class Modules_test_sequence_string_2_frame_list(unittest.TestCase):

    def runTest(self):

        self.assertEqual(S.string_2_frame_list("1-10"),
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        self.assertEqual(S.string_2_frame_list("100-500x100"),
                         [100, 200, 300, 400, 500])

        self.assertEqual(S.string_2_frame_list("1-5,8-14x2,20,21,23,26,30"),
                         [1, 2, 3, 4, 5, 8, 10, 12, 14, 20, 21, 23, 26, 30])

        self.assertEqual(S.string_2_frame_list("-5-5"),
                         [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])

        self.assertEqual(S.string_2_frame_list("-10--5"),
                         [-10, -9, -8, -7, -6, -5])

        self.assertEqual(S.string_2_frame_list("0-20x4"),
                         [0, 4, 8, 12, 16, 20])

        self.assertRaises(S.String2FrameListException,
                          S.string_2_frame_list,
                          "0-20x")

class Modules_test_sequence_string_2_padding(unittest.TestCase):

    def runTest(self):

        self.assertEqual(S.string_2_padding("10-50#"), 4)
        self.assertEqual(S.string_2_padding("200-300@@"), 2)
        self.assertEqual(S.string_2_padding("1-100@@@@@"), 5)
        self.assertEqual(S.string_2_padding("0500"), 4)
        self.assertEqual(S.string_2_padding("1-10%04"), 4)
        self.assertEqual(S.string_2_padding("00100-00500"), 5)
        self.assertEqual(S.string_2_padding("100-00500"), 5)

        self.assertRaises(S.String2PaddingException,
                          S.string_2_padding,
                          "1-100#@@@@")

if __name__ == "__main__":
    unittest.main()
