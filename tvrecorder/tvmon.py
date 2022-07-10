#
# Copyright (c) 2022, Chris Allison
#
#     This file is part of tvrecorder.
#
#     tvrecorder is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     tvrecorder is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with tvrecorder.  If not, see <http://www.gnu.org/licenses/>.
#
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
