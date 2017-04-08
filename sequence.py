
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
