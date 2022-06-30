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


def updateChannels(linupdata, eng):
    try:
        # with open("/home/chris/tmp/lineups.json", "r") as ifn:
        #     xdict = json.load(ifn)
        # xdict = json.loads(linupdata)
        xdict = linupdata
        rmap = getRMap(xdict["map"])
        labels = ["name", "callsign"]
        llabs = ["height", "width", "category", "md5", "source"]
        existstation = createdstation = 0
        existlogo = createdlogo = 0
        # outer and inner context manager for the Session object
        # the outer `session` opens the session and auto closes it
        # the inner `session.begin` starts transactions and
        # will auto commit when the code drops out of the context manager
        with Session(eng) as session, session.begin():
            for station in xdict["stations"]:
                stationid = int(station["stationID"])
                if not session.query(Channel).filter_by(stationid=stationid).first():
                    kwargs = {key: station[key] for key in labels}
                    kwargs["stationid"] = stationid
                    kwargs["channelnumber"] = rmap[stationid]
                    stat = Channel(**kwargs)
                    log.debug(f"Inserting {stat=}")
                    session.add(stat)
                    # db.session.commit()
                    createdstation += 1
                else:
                    existstation += 1
            # if "stationLogo" in station:
            #     for logo in station["stationLogo"]:
            #         if not Logo.query.filter_by(url=logo["URL"]).first():
            #             kwargs = {key: logo[key] for key in llabs}
            #             kwargs["url"] = logo["URL"]
            #             ologo = Logo(**kwargs)
            #             log.debug(f"Inserting {ologo}")
            #             db.session.add(ologo)
            #             db.session.commit()
            #             createdlogo += 1
            #         else:
            #             existlogo += 1
        log.info(
            f"Channels inserted: {createdstation}, Existing Channels: {existstation}"
        )
        # log.info(f"Logos inserted: {createdlogo}, Existing Logos: {existlogo}")
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def getRMap(xmap):
    try:
        rmap = {}
        for xm in xmap:
            rmap[int(xm["stationID"])] = int(xm["channel"])
        return rmap
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
