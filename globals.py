import os

def run():
    """
    execute the crux of the module
    """

    # open the file path in the package root
    fp = open(os.path.abspath(os.path.join(__file__, "../GLOBALS")))

    # read each entry in the file
    for l in fp.readlines():
        l = l.strip()

        # ignore commented sections
        nocomment = l.split("#", 1)[0]
        if nocomment == "":
            continue

        # set the variables in the globals
        (var, val) = nocomment.split("=")
        var = var.strip()
        val = eval(val.strip())

        globals()[var] = val

run() # automatically run on import. comment out to require manual activation