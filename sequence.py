import os, sys

# all acceptable delineations that go between the frame number and the file extension
RIGHT_SEP = "." 
# all acceptable delineations that go between the file base name and the frame number
LEFT_SEP = " ._" 
# all numbers and operations for padding and step size
NUM_OPS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", ",", "x", '#', '@', '%', 'd']


def frame_list_2_string(inlist):
    """
    takes an input list of numbers
    returns the plain text equivalent of that list
    """

    # short-circuits and input cleanup
    if inlist == []:
        return ""
    else:
        inlist.sort()

    # initialize variables
    rval = ""
    newsequence = True
    lastnum = None
    series = False
    firstdiff = None
    thisdiff = None

    # cycle through all the items in the list
    i = -1
    while 1:
        i += 1
        # break out of infinite while routine
        if i >= len(inlist):
            break

        # if this is a new sequence add a comma
        if newsequence:
            if rval != "":
                rval += ","

            # initialize the new sequence
            rval += str(inlist[i])
            newsequence = False

        # we are continuing an existing sequence
        else:
            # calculate the diff to see if we can condense this to a sequence
            firstdiff = inlist[i] - inlist[i - 1]

            if i < len(inlist) - 1:
                thisdiff = inlist[i + 1] - inlist[i]
            else:
                thisdiff = None

            if firstdiff == thisdiff:
                rval += "-"

                # continue scanning through the list to see how many numbers in this sequence match the current diff
                while 1:
                    if i == len(inlist) - 1:
                        break

                    thisdiff = inlist[i + 1] - inlist[i]
                    if firstdiff == thisdiff:
                        i += 1
                    else:
                        # if the diff doesn't match, this is the end of this sequence
                        break

                if firstdiff == 1:
                    rval += "%d" % (inlist[i])
                else:
                    rval += "%dx%d" % (inlist[i], firstdiff)

                series = False
                newsequence = True

            # if the diffs don't match, this number is on it's own
            else:
                rval += ",%d" % (inlist[i])
                series = False

    return rval
# /frame_list_2_string


class String2FrameListException(Exception):
    pass


def string_2_frame_list(instring):
    """
    takes in a string representing a human-readable sequence of numbers
     returns a list with each frame represented as a number
    """

    # initialize variables
    remainder = instring
    rval = []

    def pop_front_number(inv):
        """
        remove the next number from the front of the string
        returns the popped a tuple containing the popped number and the remainder of the string
        """

        # short circuit
        if len(inv) == 0:
            return (None, inv)

        # initialize variables
        is_neg = False
        num = None

        # check if the first character is negative
        if inv[0] == '-':
            is_neg = True
            inv = inv[1:]

        # find the end of the first number which is still a digit
        while len(inv) > 0 and inv[0].isdigit():
            if num == None:
                num = 0
            num = num * 10 + int(inv[0])
            inv = inv[1:]

        # if the number was negative, bake that back into the return val
        if is_neg:
            num = num * -1

        return (num, inv)

    # loop while there is still string to work on
    lastnumber = None
    while len(remainder) > 0:
        # check if we have a number that needs to be popped off the front
        if remainder[0].isdigit() or (remainder[0] == "-" and lastnumber is None):
            (lastnumber, remainder) = pop_front_number(remainder)

            # this was the last number, so append it and continue to break out of the while
            if remainder == "":
                rval.append(lastnumber)
                continue

        # there is a last number, so this - represents a sequence
        elif remainder[0] == "-":
            (thisnumber, remainder) = pop_front_number(remainder[1:])
            if thisnumber is None:
                continue

            # if there is a x after the sequence representing a step factor, process it
            if len(remainder) > 0 and remainder[0] == "x":
                (step, remainder) = pop_front_number(remainder[1:])
                if step is None:
                    raise String2FrameListException("step value missing")

                # we have a valid sequence, append the numbers
                rval += range(lastnumber, thisnumber + 1, step)

            # there is no step value, so assume 1
            else:
                rval += range(lastnumber, thisnumber + 1)

            lastnumber = None

        # if there is a remainder with additional sequences to process
        # remove the comma and let the loop continue
        elif remainder[0] == ",":
            if lastnumber is not None:
                rval.append(lastnumber)
            remainder = remainder[1:]
        else:
            remainder = remainder[1:]

    return rval
# /frameString2List


class String2PaddingException(Exception):
    pass


def string_2_padding(instring):
    """
    takes in a string describing the frame numbers
    extracts and returns the padding on the frame numbers
    """

    parsestring = instring
    padding = None

    # if just a single number is present, the length of the string is the padding
    if parsestring.isdigit():
        return len(parsestring)

    # run through the string to pull out the padding
    while len(parsestring) > 0:
        # print "### process", parsestring

        # we are to the padding description part of the string
        if parsestring[0] == '#' or parsestring[0] == '@' or parsestring[0] == '%':

            # error, there's two padding descript
            if padding is not None:
                raise String2PaddingException("more than one padding string found in %s" % repr(instring))

            # process a pound symbol
            if parsestring[0] == '#':
                padding = 4

            # process an ampersand
            elif parsestring[0] == '@':
                padding = 1
                parsestring = parsestring[1:]
                while len(parsestring) > 0 and parsestring[0] == '@':
                    padding += 1
                    parsestring = parsestring[1:]

            # process a % expression
            elif parsestring[0] == '%':
                parsestring = parsestring[1:]
                if parsestring[0] != '0':
                    raise String2PaddingException("invalid nuke style padding in %s (i.e. %%04d is valid)" % instring)
                else:
                    parsestring = parsestring[1:]
                numstr = ""
                while len(parsestring) > 0 and parsestring[0].isdigit():
                    numstr += parsestring[0]
                    parsestring = parsestring[1:]
                padding = int(numstr)

        parsestring = parsestring[1:]

    # if there was no padding character, try to pull the padding from the numbers
    # e.g. 0100-0250
    if padding is None:
        parsestring = instring

        # loop through the parse string
        while len(parsestring) > 0:

            # this is a number, see how long it is
            if parsestring[0].isdigit():
                thispadding = 1
                parsestring = parsestring[1:]
                while len(parsestring) > 0 and parsestring[0].isdigit():
                    thispadding += 1
                    parsestring = parsestring[1:]
                if padding is None or thispadding > padding:
                    padding = thispadding

            # if we aren't looking at a number, throw it away, we don't care
            else:
                parsestring = parsestring[1:]

    return padding
# /string_2_padding


class SequenceFormatException(Exception):
    pass


def seq(path, frames=None):
    """
    helper function to get rid of a bit of typing
    """
    return sequence(path, frames)

class sequence(object):
    def __init__(self, path, inframes=None):
        # sanity check the input
        if not type(path) == type(""):
            raise SequenceFormatException("sequence constructor takes a string path")
        elif not (len(path) > 0):
            raise SequenceFormatException("sequence path cannot be an empty string")

        # normalize the path
        path = os.path.abspath(path)

        # split off the directory and the remainder
        (self.directory, filepart) = os.path.split(path)

        noext = True
        extlen = 999999
        # pull the extension
        for each in RIGHT_SEP:
            # find the separator than produces the smallest ext piece
            pieces = filepart.rsplit(each, 1)
            
            # verify a split occured
            if len(pieces) == 2 and len(pieces[1]) < extlen:
                # set all the variables for this scenario
                (left, ext) = pieces
                extlen = len(ext)
                rsep = each
                noext = False
                
        # if no ext was found at all using the split method
        if noext:
            left = filepart
            prefix = filepart
            ext = ''
            rsep = ''

        noframes = True
        numlen = 999999
        # pull the prefix
        for each in LEFT_SEP:
            # find the split that produces the largest prefix
            # and smallest num part
            pieces = left.rsplit(each, 1)

            # verify a split occurred
            if len(pieces) == 2 and len(pieces[1]) < numlen:

                # detect if the number part doesn't actually
                # contain a number (we will determine it later)
                if pieces[1] == '' or pieces[1] == '*':
                    noframes = False

                # otherwise, scan the num part to determine everything
                # is valid, and we can say we found what we need
                else:
                    for c in pieces[1]:
                        if not c in NUM_OPS:
                            break
                        noframes = False

                # everything checked out, so this is a valid split,
                # set the variables
                if noframes == False:
                    (prefix, framepiece) = pieces
                    numlen = len(framepiece)
                    lsep = each

        # if we faile to find a number part (e.g. with a single mov
        # file), set value
        if noframes:
            prefix = left
            lsep = ''
            frames = []
            padding = None

        # set the class values based on what we have so far
        self.prefix = prefix
        self.lsep = lsep
        self.rsep = rsep
        self.ext = ext

        # process the frame numbers if provided
        if inframes is not None:

            # sanity check the input
            if type(inframes) == type([]):
                try:
                    # normalize the values
                    frames = [int(f) for f in inframes]
                except:
                    raise SequenceFormatException("input frames need to either be a string, or a list of integers or strings")

            # if it is a string, process it to a frame list
            elif type(inframes) == type(""):
                # pull the frame list from the string
                frames = string_2_frame_list(inframes)

                # pull the padding from the string
                padding = string_2_padding(inframes)

        else:
            # there is nothing in the string to indicate the frame numbers
            if noframes == False and framepiece == "":
                frames = []
                padding = None

            # otherwise, we just need to parse the frame part of the file descriptor
            elif noframes == False:
                # pull the frame list from the number string
                frames = string_2_frame_list(framepiece)

                # pull the frame padding
                padding = string_2_padding(framepiece)

        # set the rest of the class variables
        self.frames = frames
        self.padding = padding

        # determine if we need to retrieve the frame numbers because
        # they weren't expressly set
        if frames == [] and padding is None and noframes == False:
            self.getFrames()

        return

    def isSingleFile(self):
        """
        returns if this object describes a single file
        e.g. file.mov
        """

        if len(self.frames) < 2:
            return True
        return False

# /sequence class

