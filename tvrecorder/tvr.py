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
"""recorder module for tvrecorder."""
from datetime import datetime
from pathlib import Path
import subprocess
import sys

from ccaerrors import errorNotify

from tvrecorder.strings import cleanString


def dtToTs(sdate):
    """Convert a date/time string into a timestamp

    args: sdate: date/time string
                "2022-05-14T14:27:00"
    """
    try:
        dt = datetime.fromisoformat(sdate)
        return int(dt.timestamp())
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def tsToDt(ts):
    try:
        return datetime.fromtimestamp(ts)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def recordProgram(
    title,
    channel="BBC TWO",
    start=0,
    end=3600,
    frontpadding=120,
    endpadding=900,
    adaptor=0,
    basedir="/run/media/chris/seagate4/TV/tv/",
):
    try:
        kwargs = {
            "channel": channel,
            "start": start,
            "length": int((end - start) + frontpadding + endpadding),
            "adaptor": adaptor,
            "basedir": basedir,
        }
        cmd = buildRecordCommand(title, **kwargs)
        res = subprocess.run(cmd)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def buildRecordCommand(
    title,
    channel="BBC TWO",
    start=0,
    length=3600,
    adaptor=0,
    basedir="/run/media/chris/seagate4/TV/tv/",
):
    """Builds the dvbv5-zap command ready for subprocess

    args: channel: str - name of the channel from the dvb_channel.conf file
          title: str - title of the program
          start: int - timestamp of the start time
          length: int - Full length of the recording including padding
          adaptor: int - the adaptor number (0-3) to use
          basedir: str - recordings directory
    returns: the command list as required by subprocess.run()
    """
    try:
        then = datetime.fromtimestamp(start)
        schan = cleanString(channel)
        stitle = cleanString(title)
        rdir = Path(f"{basedir}/{stitle}")
        rdir.mkdir(parents=True, exist_ok=True)
        tstamp = then.strftime("%Y%m%dT%H%M")
        fqfn = Path(f"{basedir}/{stitle}/{tstamp}-{schan}-{stitle}.ts")
        # length = int(end - start)
        # padding = 120 + 900
        # actualstart = start - 120
        cmd = f"dvbv5-zap -c /home/chris/.tzap/dvb_channel.conf -a {adaptor} -p -r "
        cmd += f"-t {int(length)}"
        lcmd = cmd.split(" ")
        lcmd.append("-o")
        lcmd.append(fqfn)
        lcmd.append(channel)
        return lcmd
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


if __name__ == "__main__":
    kwargs = {
        "channel": "BBC ONE East E",
        "start": 0,
        "length": 123,
        "adaptor": 0,
        "basedir": "/home/chris/tv/test",
    }
    lst = buildRecordCommand("Some Title", **kwargs)
    for x in lst:
        print(x)

    del kwargs["length"]
    kwargs["frontpadding"] = 0
    kwargs["endpadding"] = 0
    kwargs["end"] = 123
    kwargs["frontpadding"] = 0
    kwargs["endpadding"] = 0
    recordProgram("Some Other Title", **kwargs)
