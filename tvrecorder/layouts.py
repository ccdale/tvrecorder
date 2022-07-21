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
"""layouts module for tvrecorder"""
import sys

from ccaerrors import errorNotify, errorRaise

from tvrecorder.strings import durationString, timeString


def programLine(schedule, withchannel=False, maxchanlen=20, maxtitlelen=40, nextkey=0):
    try:
        dprog = schedule["dprog"]
        dchan = schedule["dchan"]
        xstart = timeString(schedule["airdate"])
        duration = durationString(schedule["duration"])
        line = []
        if withchannel:
            line.append(
                sg.T(
                    f"{dchan['name'][:maxchanlen]}",
                    size=maxchanlen,
                    justification="left",
                    enable_events=True,
                    metadata=f"{dchan['stationid']}",
                    key=f"pl-{nextkey}",
                )
            )
        line.append(sg.T(f"{xstart:>6}", size=6, justification="right"))
        line.append(sg.T(f"{duration:>6}", size=8, justification="right"))
        line.append(
            sg.T(
                f"{dprog['title'][:maxtitlelen]}",
                size=maxtitlelen,
                justification="left",
                enable_events=True,
                metadata=f"{schedule['md5']}",
                key=f"s-{nextkey}",
            )
        )
        line.append(sg.T(f"{dprog['shortdesc']}", justification="left"))
        return line
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def programLineHeadings(withchannel=False, maxchanlen=20, maxtitlelen=40):
    try:
        line = []
        if withchannel:
            line.append(sg.T("Channel", size=maxchanlen, justification="left"))
        line.append(sg.T("Start", size=6, justification="right"))
        line.append(sg.T("Duration", size=8, justification="right"))
        line.append(sg.T("Title", size=maxtitlelen, justification="left"))
        line.append(sg.T("Description", justification="left"))
        return line
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
