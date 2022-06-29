#
# Copyright (c) 2018, Centrica Hive Ltd.
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
"""Updated DB module for tvrecorder."""
import sys

from ccaerrors import errorNotify

from tvrecorder.credential import makeSDCreds
from tvrecorder.config import Configuration
from tvrecorder.db import makeDBEngine


def updatedb():
    try:
        cf = Configuration(appname="tvrecorder")
        mysqleng = makeDBEngine(cf)
        uname, pword, token, tokenexpires = makeSDCreds(cf)
        cf.writeConfig()
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
