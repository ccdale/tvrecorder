"""recorder module for tvrecorder."""
from datetime import datetime
from pathlib import Path
import subprocess
import sys

from ccaerrors import errorNotify


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


def buildRecordCommand(channel, title, start, end, adaptor=0):
    """Builds the dvb5-zap command ready for subprocess

    args: channel: str - name of the channel from the dvb_channel.conf file
          title: str - title of the program
          start: int - timestamp of the start time
          end: int - timestamp of the end time
          adaptor: int - the adaptor number (0-3) to use
    returns: the command list as required by subprocess.run()
    """
    try:
        then = datetime.fromtimestamp(start)
        basedir = "/home/chris/run/media/chris/seagate4/TV/tv/"
        schan = channel.replace(" ", "_")
        stitle = title.replace(" ", "_")
        rdir = Path(f"{basedir}/{stitle}")
        rdir.mkdir(parents=True, exists_ok=True)
        tstamp = then.strftime("%Y%m%dT%H%M")
        fqfn = Path(f"{basedir}/{stitle}/{tstamp}-{schan}-{stitle}.ts")
        length = int(end - start)
        padding = 120 + 900
        actualstart = start - 120
        cmd = f"dvb5-zap -c ~/.tzap/dvb_channel.conf -a {adaptor} -p -r "
        cmd += f"-t {int(length + padding)} "
        lcmd = cmd.split(" ")
        lcmd.append("-o")
        lcmd.append(fqfn)
        lcmd.append(channel)
        return lcmd
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


if __name__ == "__main__":
    lst = buildRecordCommand(
        "BBC TWO", "Some Magic Title", 1655626624, 1655630224, adaptor=2
    )
    for x in lst:
        print(x)
