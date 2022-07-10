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
"""Channel mapper for tvrecorder."""
import configparser
import os
import sys

from ccaerrors import errorNotify, errorExit
import ccalogging

from tvrecorder import __version__, __appname__
from tvrecorder.config import Configuration
from tvrecorder.db import makeDBEngine
from tvrecorder.wrangler import mapToDVB

ccalogging.setLogFile("/home/chris/channelmapper.out")
ccalogging.setInfo()
log = ccalogging.log


def begin(appname, debug=False):
    try:
        cf = Configuration(appname=appname)
        mysqleng = makeDBEngine(cf, echo=debug)
        zap = configparser.ConfigParser()
        home = os.path.expanduser("~/")
        tzap = os.path.join(home, ".tzap", "dvb_channel.conf")
        zap.read(tzap)
        return (cf, mysqleng, zap)
    except Exception as e:
        errorExit(sys.exc_info()[2], e)


def channelmapper():
    try:
        debug = True
        cf, mysqleng, zap = begin(__appname__, debug=debug)
        mapToDVB(mysqleng, zap)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


if __name__ == "__main__":
    channelmapper()
