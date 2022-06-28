"""TV monitor module for tvrecorder application."""
import sys

from ccaconfig.config import ccaConfig
from ccaerrors import errorNotify, errorRaise, errorExit


def mon():
    try:
        kwargs = {"appname": "tvrecorder", "defaultd": None, "overrided": None}
        cf = ccaConfig(**kwargs)
        cfg = cf.envOverride()
        print(f"{cfg=}")
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


if __name__ == "__main__":
    mon()
