#
# Copyright (c) 2021, Christopher Allison
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
import sys

import PySimpleGUI as sg
from ccaerrors import errorNotify, errorRaise

from tvrecorder.layouts import programLine, programLineHeadings
from tvrecorder.strings import durationString, timeString
from tvrecorder.wrangler import favourites, whatsOnNow, chanProgs


def credsWindow(username):
    try:
        log.debug("opening credentials window.")
        layout = [
            [sg.T("Password will stored in the system keyring.")],
            [sg.T("SD Username"), sg.I(username, key="UIN")],
            [sg.T("SD Password"), sg.I(key="PIN")],
            [sg.Submit(key="submit"), sg.Cancel(key="cancel")],
        ]
        window = sg.Window("Schedules Direct Credentials.", layout)
        event, values = window.read()
        window.close()
        log.debug("credentials window closed.")
        un = pw = None
        if event == "submit":
            un = values["UIN"]
            pw = values["PIN"]
        if "PIN" in values:
            values["PIN"] = "xxxxxxxxxx"
        log.debug(f"event: {event}, values: {values}")
        return un, pw
    except Exception as e:
        errorRaise(sys.exc_info()[2], e)


def errorWindow(emsg):
    try:
        layout = [[sg.T(emsg)], [sg.Cancel()]]
        win = sg.Window("Error", layout)
        event, values = win.read()
        win.close()
    except Exception as e:
        errorRaise(sys.exc_info()[2], e)


def chanWindow(engine, favs=True):
    try:
        favs = favourites(engine, favs=favs)
        chans = [
            [
                sg.T(x["channelnumber"], size=4, justification="right"),
                sg.T(x["name"], key=x["stationid"], enable_events=True),
            ]
            for x in favs
        ]
        layout = [
            [sg.T("Pick a Channel")],
            chans,
            [sg.Cancel()],
        ]
        win = sg.Window("test chans", layout)
        event, values = win.read()
        print(f"{event=}, {values=}")
        win.close()
        for fav in favs:
            if fav["stationid"] == event:
                print(f"channel: {fav['name']}")
                break
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def mainWindow(engine):
    try:
        scheds = whatsOnNow(engine)
        layout = [programLineHeadings(withchannel=True)]
        layout.extend(
            [
                programLine(x, withchannel=True, nextkey=nk)
                for nk, x in enumerate(scheds)
            ]
        )
        layout.append([sg.Cancel()])
        win = sg.Window("On Now", layout)
        while True:
            event, values = win.read()
            print(f"{event=}, {values=}")
            if event == "Cancel" or sg.WIN_CLOSED:
                break
            elif event.startswith("pl-"):
                # retrieve the chanid from the program line metadata
                chanid = win.find_element(event).metadata
                # tmp = event.split("-")
                # chanid = tmp[1]
                print(f"{chanid=}")
                channelProgramsWindow(engine, chanid)
            elif event.startswith("s-"):
                # retrieve the schedule md5 from the program line metadata
                pass
        win.close()
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def channelProgramsWindow(engine, chanid, maxlines=35):
    try:
        scheds = chanProgs(engine, chanid, limit=maxlines)
        # print(f"{scheds=}")
        if len(scheds):
            channame = scheds[0]["dchan"]["name"]
        layout = [programLineHeadings(withchannel=True)]
        layout.extend([programLine(x, nextkey=nk) for nk, x in enumerate(scheds)])
        if len(layout) > maxlines:
            layout = layout[:maxlines]
        layout.append([sg.Cancel()])
        win = sg.Window(f"{channame}", layout)
        event, values = win.read()
        print(f"{event=}, {values=}")
        win.close()
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
