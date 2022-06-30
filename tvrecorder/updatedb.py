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

from ccaerrors import errorNotify, errorExit
import ccalogging
from sqlalchemy.orm import Session

from tvrecorder import __version__, __appname__
from tvrecorder.credential import getSDCreds
from tvrecorder.config import Configuration
from tvrecorder.db import makeDBEngine
from tvrecorder.models import Channel
from tvrecorder.sdapi import SDApi
from tvrecorder.wrangler import updateChannels

ccalogging.setConsoleOut()
log = ccalogging.log


def linupRefresh(sd, cf, eng, force=False):
    try:
        for lineup in sd.lineups:
            if sd.getTimeStamp(lineup["modified"]) > cf.get("lineupdate", 0) or force:
                log.info(f"Lineup changes detected: refreshing lineup {lineup}")
                lineupdata = sd.getLineup(lineup["lineup"])
                updateChannels(lineupdata, eng)
                cf.set("lineupdate", sd.getTimeStamp(lineup["modified"]))
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def begin(appname, debug=False):
    try:
        cf = Configuration(appname=appname)
        mysqleng = makeDBEngine(cf, echo=debug)
        uname, pword, token, tokenexpires = getSDCreds(cf)
        if tokenexpires is None:
            tokenexpires = 0
        kwargs = {
            "username": uname,
            "password": pword,
            "appname": appname,
            "token": token,
            "tokenexpires": tokenexpires,
            "debug": debug,
        }
        sd = SDApi(**kwargs)
        sd.apiOnline()
        if not sd.online:
            raise Exception("Schedules Direct does not appear to be online.")
        return (cf, sd, mysqleng)
    except Exception as e:
        errorExit(sys.exc_info()[2], e)


def close(cf, sd):
    try:
        cf.set("token", sd.token)
        cf.set("tokenexpires", sd.tokenexpires)
        cf.writeConfig()
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def updatedb():
    try:
        debug = True
        cf, sd, mysqleng = begin(__appname__, debug=debug)
        linupRefresh(sd, cf, mysqleng)
        close()
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


if __name__ == "__main__":
    updatedb()
