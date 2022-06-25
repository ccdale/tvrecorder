import sys

from ccaerrors import errorNotify


def cleanString(istring):
    """Replaces 'nasty' chars in strings that could be used as filenames"""
    try:
        remove = "/(){}@~!£$%^&*+='\""
        for i in remove:
            istring = istring.replace(i, "")
        istring = istring.replace(" ", "_")
        while "__" in istring:
            istring = istring.replace("__", "_")
        while "--" in istring:
            istring = istring.replace("--", "-")
        istring = istring.replace("_-_", "-")
        istring = istring.replace("-_-", "_")
        return istring
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
