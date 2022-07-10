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

from tvrecorder.wrangler import favourites


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


def chanWindow(engine):
    try:
        favs = favourites(engine)
        print(favs)
        chans = [[x["channelnumber"], x["name"]] for x in favs]
        layout = [[sg.T("test chans")], [sg.Cancel()], [sg.Listbox(values=chans)]]
        win = sg.Window("test chans", layout)
        win.close()
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
