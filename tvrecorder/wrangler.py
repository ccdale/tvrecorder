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
"""Data wrangler module for tvrecorder."""
import sys

from ccaerrors import errorNotify, errorExit

from tvrecorder.models import Channel, Schedulemd5, Schedule


def addUpdateSMD5(sd, smd5, chanid, xdate, session):
    try:
        md5 = session.query(Channel).filter_by(md5=smd5["md5"]).first()
        if md5:
            return False
        sdate = f"{xdate}T00:00:00Z"
        datets = sd.getTimeStamp(sdate)
        kwargs = {
            "md5": smd5["md5"],
            "stationid": chanid,
            "datets": datets,
            "modified": sd.getTimeStamp(smd5["lastModified"]),
        }
        md5 = Schedulemd5(**kwargs)
        session.add(md5)
        return True
    except Exception as e:
        msg = f"{e}\n{smd5=}, {chanid=}, {xdate=}\n"
        msg += f"{kwargs=}"
        errorExit(sys.exc_info()[2], msg)


def schedulesMd5(sd):
    try:
        retrieve = {}
        xall = Station.query.all()
        clist = Station.query.filter_by(getdata=1).all()
        log.info(f"retrieving MD5 hashes for {len(clist)} / {len(xall)} channels")
        slist = [x.stationid for x in clist]
        smd5 = sd.getScheduleMd5(slist)
        for chan in smd5:
            log.debug(f"scheduleMd5: {chan=}")
            for xdate in smd5[chan]:
                log.debug(f"scheduleMd5: {xdate=}")
                if addUpdateSMD5(sd, smd5[chan][xdate], chan, xdate):
                    if chan not in retrieve:
                        retrieve[chan] = []
                    retrieve[chan].append(xdate)
        log.debug(f"sheduleMd5 returns: {retrieve=}")
        return retrieve
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
