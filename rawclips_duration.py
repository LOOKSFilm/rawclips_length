from EditShareAPI import EsAuth, FlowMetadata
import json
from timecode import Timecode
from datetime import datetime, timedelta

EsAuth.login("10.0.77.13", "christoph", "looksfilm")

mediaspaces = ["OCF OAF"]

def pprint(data):
    print(json.dumps(data, indent=4))

def calc_duration(duration):
    hours, minutes, seconds, frames, str_fps = map(str, str(duration).split(":"))
    fps = float(str_fps.split("/")[0]) / float(str_fps.split("/")[1])
    seconds = float(seconds)
    seconds += float(frames) / float(fps)
    total_seconds = float(hours) * 3600 + float(minutes) * 60 + float(seconds)
    time_delta = timedelta(seconds=total_seconds)
    return time_delta

for mediaspace in mediaspaces:
    assets = FlowMetadata.getMediaSpaceClips(mediaspace)

clip_ids = []
for asset in assets:
    if "clip_id" in asset.keys():
        clip_ids.append(asset["clip_id"])

total_duration = timedelta()
for clip_id in clip_ids:
    metadata = FlowMetadata.getClipData(clip_id)
    if "error" in metadata.keys():
        continue
    if not metadata["has_video"]:
        continue
    if metadata["status_text"] == "Archived":
        #pprint(metadata["gone_locations"][0]["userpath"])
        pprint(metadata["video"][0]["file"]["archive_locations"][0]["userpath"])
    else:
        pprint(metadata["video"][0]["file"]["locations"][0]["userpath"])

    # total_duration += calc_duration(metadata["video"][0]["timecode_duration"])
    # print(total_duration)


