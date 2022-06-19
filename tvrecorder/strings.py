import sys

from ccaerrors import errorNotify


def cleanString(istring):
    """Replaces 'nasty' chars in strings that could be used as filenames"""
    try:
        replace = "/(){}@~!£$%^&*+='\""
        for i in replace:
            istring = istring.replace(i, "")
        istring.replace(" ", "_")
        while "__" in istring:
            istring.replace("__", "_")
        while "--" in istring:
            istring.replace("--", "-")
        return istring
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
