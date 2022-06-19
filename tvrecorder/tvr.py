"""recorder module for tvrecorder."""
from datetime import datetime
from pathlib import Path
import sys

from ccaerrors import errorNotify


def buildRecordCommand(channel, title, start, end, adaptor=0):
    try:
        then = datetime.fromtimestamp(start)
        basedir = "/run/media/chris/seagate4/TV/tv/"
        schan = channel.replace(" ", "_")
        stitle = title.replace(" ", "_")
        rdir = Path(f"{basedir}/{stitle}")
        rdir.mkdir(parents=True)
        tstamp = then.strftime("%Y%m%dT%H%M")
        fqfn = Path(f"{basedir}/{stitle}/{tstamp}-{schan}-{stitle}.ts")
        length = int(start - end)
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
