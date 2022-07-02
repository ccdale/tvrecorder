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
"""Channel mapper for tvrecorder."""
import configparser
import os
import sys

from ccaerrors import errorNotify, errorExit
import ccalogging

from tvrecorder import __version__, __appname__
from tvrecorder.config import Configuration
from tvrecorder.db import makeDBEngine
from tvrecorder.wrangler import getAllChannels, setMappedChannels

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


def searchZap(zap, search):
    try:
        poss = []
        found = False
        for sect in zap.sections():
            if search.lower()[:4] == sect.lower()[:4]:
                poss.append[sect]
            elif search == sect:
                found = True
                break
        return (poss, found)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def chooseName(poss, chan):
    try:
        for n in poss:
            print(n)
        print("Type the correct DVB name for channel {chan}")
        choice = input("? ")
        return choice
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def channelmapper():
    try:
        debug = False
        cf, mysqleng, zap = begin(__appname__, debug=debug)
        chans = getAllChannels(mysqleng)
        updates = []
        for chan in chans:
            if len(chan.dvbname) > 0:
                continue
            poss, found = searchZap(zap, chan.name)
            if found:
                print(f"Channel {chan.name} - name found exactly in zap")
                chan.dvbname = chan.name
                updates.append(chan)
                continue
            # choose which one
            choice = chooseName(poss, chan.name)
            if len(choice) == 0:
                break
            chan.dvbname = choice
            updates.append(chan)
        setMappedChannels(eng, updates)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


if __name__ == "__main__":
    channelmapper()
