
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

def string_2_frame_list(instring):
    """
    takes in a string representing a human-readable sequence of numbers
     returns a list with each frame represented as a number
    """

    # initialize variables
    remainder = instring
    rval = []

    def popNumber(inv):
        """

        """

        # initialize variables
        is_neg = False
        num = None

        if inv[0] == '-':
            is_neg = True
            inv = inv[1:]
        while len(inv) > 0 and inv[0].isdigit():
            if num == None:
                num = 0
            num = num * 10 + int(inv[0])
            inv = inv[1:]
        if is_neg:
            num = num * -1
        return (num, inv)

    lastnumber = None
    while len(remainder) > 0:
        if remainder[0].isdigit() or (remainder[0] == "-" and lastnumber is None):
            (lastnumber, remainder) = popNumber(remainder)
            if remainder == "":
                rval.append(lastnumber)
        elif remainder[0] == "-":
            (thisnumber, remainder) = popNumber(remainder[1:])
            if thisnumber is None:
                continue
            if len(remainder) > 0 and remainder[0] == "x":
                (step, remainder) = popNumber(remainder[1:])
                # if step is None:
                #     genericErr()
                rval += range(lastnumber, thisnumber + 1, step)
            else:
                rval += range(lastnumber, thisnumber + 1)
            lastnumber = None
        elif remainder[0] == ",":
            if lastnumber is not None:
                rval.append(lastnumber)
            remainder = remainder[1:]
        else:
            remainder = remainder[1:]

    return rval
# /frameString2List

