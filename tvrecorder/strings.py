#
# Copyright (c) 2018, Chris Allison
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
