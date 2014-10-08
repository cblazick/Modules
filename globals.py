import os

def run():
    fp = open(os.path.abspath(os.path.join(__file__, "../GLOBALS")))
    for l in fp.readlines():
        l = l.strip()
        nocomment = l.split("#", 1)[0]
        if nocomment == "":
            continue

        (var, val) = nocomment.split("=")
        var = var.strip()
        val = eval(val.strip())

        globals()[var] = val
