#!/usr/bin/python

import os, sys
import smtplib, socket
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import subprocess
import globals

METHODS = { "SMTP" : 1,    # using the standard smtplib.SMTP() call
            "msmtp" : 2,   # nas4free uses msmtp to send email. it doesn't receive smtp connections, it only sends them
            "sendmail" : 3
}

class Emailer:
    """
    class for building and sending emails
    """

    sendFunc = None

    def __init__(self, f, t, s, b, method=None):
        """
        initialize an email to send
        """

        self.fromLine = f
        self.toLine = t
        self.subjectLine = s
        self.body = b

        if method is None:
            self.method = globals.EMAIL_SEND_METHOD
        else:
            self.method = method

    def sendMail_SMTP(self):
        """
        SMTP specific function for sending the email
        """

        # build the header / message
        message = "\n".join(["From: " + self.fromLine,
                             "To: " + ", ".join(self.toLine),
                             "Subject: " + self.subjectLine,
                             "",
                             self.body])

        # execute the SMTP calls and print errors if thrown
        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(self.fromLine, self.toLine, message)
            # print "Successfully sent email"
        except smtplib.SMTPException:
            print "ERROR: unable to send email"
            raise
        except socket.error:
            print "ERROR: unable to connect to SMTP server"
            raise

    def sendMail_msmtp(self):
        """
        msmtp specific function for sending email

        this supports a nas4free installation that did not have a traditional SMTP daemon
        """

        # make sure bash is used for the printf command
        cmd = "/bin/bash -c \""
        # print the header to get piped into the msmtp command
        cmd += "printf 'From: %s\n" % (self.fromLine)
        cmd += "To: %s\n" % (", ".join(self.toLine))
        cmd += "Subject: %s\n" % (self.subjectLine)
        cmd += "\n%s'"  % (self.body)
        # call the msmtp command with the NAS4FREE config file
        cmd += " | sudo msmtp -C /var/etc/msmtp.conf"
        # add to's to the command (header isn't actually used)
        for e in self.toLine:
            cmd += " -t %s" % (e)
        cmd += "\""

        subprocess.call(cmd, shell=True)

    def sendMail_sendmail(self):
        """
        sendmail specific function for sending the email
        """

        message = MIMEMultipart('alternative')

        message.add_header('Subject', self.subjectLine)
        message.add_header('From', self.fromLine)
        message.add_header('To', ", ".join(self.toLine))

        message.attach(MIMEText(self.body))

        s = subprocess.Popen('sendmail ' + " ".join(self.toLine), shell=True, stdin=subprocess.PIPE)
        s.communicate(message.as_string())

    def send(self):
        """
        switches between functions to achieve the desired method
        """

        if self.method == METHODS["SMTP"]:
            self.sendMail_SMTP()
        elif self.method == METHODS["msmtp"]:
            self.sendMail_msmtp()
        elif self.method == METHODS["sendmail"]:
            self.sendMail_sendmail()


def sendMail(fromLine, toLine, subject, body, method=None):
    if method is None:
        method = globals.EMAIL_SEND_METHOD
    e = Emailer(fromLine, toLine, subject, body, method)
    e.send()