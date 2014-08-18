#!/usr/bin/python

import os, sys

class DidYouMean:
    """
    methods for brute force generating and suggesting possible alternate spellings for what was entered
    """

    def __init__(self, dictionary=None):
        """
        initializer with optional dictionary of "correct" terms to search amongst
        """

        if dictionary is None:
            # in the future, use the english dictionary as a default
            raise NotImplementedError("In the future, default will be the english dictionary")
        else:
            if type(dictionary) != type([]):
                raise TypeError("dictionary input needs to be a list of dictionary words")
            self.dictionary = dictionary

    def process(self, word):
        """
        process a word for likely alternatives.  returns the most likely
        alternative, or the same word if found in the dictionary
        """

        if word in self.dictionary:
            # if word is already "correct", short-circuit
            return word
        elif word == "":
            # short-circuit on a blank word
            return ""
        else:
            rval = []
            editList = edits(word)
            # only add edits in the dictionary to the return list
            for e in editList:
                if e in self.dictionary:
                    if e not in rval:
                        rval.append(e)

            if rval == []:
                # no results found with one edit, try with two
                for o in editList:
                    for e in edits(o):
                        if e in self.dictionary:
                            if e not in rval:
                                rval.append(e)

            if len(rval) == 0:
                return None

            return rval

def edits(word):
    """
    the crux of the module.  generates lists of words with common typos
    to compare to the dictionary
    """

    if word == "":
        # short-circuit on a blank word
        return ""

    typos = [chr(i) for i in range(33, 127)] # upper-case, lower-case, numbers, and a bunch of punctuations

    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in typos if b]
    inserts    = [a + c + b     for a, b in splits for c in typos]
    rval = deletes + transposes + replaces + inserts

    return rval
