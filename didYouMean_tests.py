import unittest
import didYouMean

class DidYouMean_testSuite(unittest.TestCase):
    """
    testing routines for the DidYouMean module
    """

    def setUp(self):
        # add a dictionary of just a few acceptable words
        dictionary = ["one", "two", "three", "four", "five"]
        self.c = didYouMean.DidYouMean(dictionary)

    def test_edits(self):
        self.assertRaises(TypeError, didYouMean.edits, ())
        self.assertEqual(didYouMean.edits(""), "")
        self.assertEqual(sorted(didYouMean.edits("a")), sorted(['', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '!a', '"a', '#a', '$a', '%a', '&a', "'a", '(a', ')a', '*a', '+a', ',a', '-a', '.a', '/a', '0a', '1a', '2a', '3a', '4a', '5a', '6a', '7a', '8a', '9a', ':a', ';a', '<a', '=a', '>a', '?a', '@a', 'Aa', 'Ba', 'Ca', 'Da', 'Ea', 'Fa', 'Ga', 'Ha', 'Ia', 'Ja', 'Ka', 'La', 'Ma', 'Na', 'Oa', 'Pa', 'Qa', 'Ra', 'Sa', 'Ta', 'Ua', 'Va', 'Wa', 'Xa', 'Ya', 'Za', '[a', '\\a', ']a', '^a', '_a', '`a', 'aa', 'ba', 'ca', 'da', 'ea', 'fa', 'ga', 'ha', 'ia', 'ja', 'ka', 'la', 'ma', 'na', 'oa', 'pa', 'qa', 'ra', 'sa', 'ta', 'ua', 'va', 'wa', 'xa', 'ya', 'za', '{a', '|a', '}a', '~a', 'a!', 'a"', 'a#', 'a$', 'a%', 'a&', "a'", 'a(', 'a)', 'a*', 'a+', 'a,', 'a-', 'a.', 'a/', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a:', 'a;', 'a<', 'a=', 'a>', 'a?', 'a@', 'aA', 'aB', 'aC', 'aD', 'aE', 'aF', 'aG', 'aH', 'aI', 'aJ', 'aK', 'aL', 'aM', 'aN', 'aO', 'aP', 'aQ', 'aR', 'aS', 'aT', 'aU', 'aV', 'aW', 'aX', 'aY', 'aZ', 'a[', 'a\\', 'a]', 'a^', 'a_', 'a`', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak', 'al', 'am', 'an', 'ao', 'ap', 'aq', 'ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay', 'az', 'a{', 'a|', 'a}', 'a~']))

    def test_process(self):
        self.assertEqual(self.c.process("tree"), ["three"])
        self.assertEqual(sorted(self.c.process("foo")), sorted(["two", "four"]))
        self.assertEqual(self.c.process("abcd"), None)

if __name__ == "__main__":
    unittest.main()