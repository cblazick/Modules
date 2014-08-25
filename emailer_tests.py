import unittest
import emailer

class email_testSuite(unittest.TestCase):
    """
    testing routines for the email module
    """

    def setUp(self):
        self.f = "example1@gmail.com"
        self.t = ["example2@gmail.com", "example3@gmail.com"]
        self.s = "Test Email"
        self.b = "testing, testing, 1, 2, 3"

    def test_emailSMTP(self):
        print "WARNING: This will generate email to these addresses:", repr(self.t)
        raw_input("Press enter to continue")

        emailer.sendMail(self.f, self.t, self.s, self.b, method=1)

    def test_emailMsmtp(self):
        print "WARNING: This will generate email to these addresses:", repr(self.t)
        raw_input("Press enter to continue")

        emailer.sendMail(self.f, self.t, self.s, self.b, method=2)

    def test_emailSendmail(self):
        print "WARNING: This will generate email to these addresses:", repr(self.t)
        raw_input("Press enter to continue")

        emailer.sendMail(self.f, self.t, self.s, self.b, method=3)

if __name__ == "__main__":
    unittest.main()