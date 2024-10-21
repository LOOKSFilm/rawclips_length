from EditShareAPI import EsAuth, FlowMetadata
import json
from timecode import Timecode
from datetime import datetime, timedelta

EsAuth.login("10.0.77.13", "christoph", "looksfilm")

mediaspaces = ["OCF OAF"]

field = FlowMetadata.getCustomMetadataFields().fields_dict

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
print(len(assets))
clip_ids = []
for asset in assets:
    if "clip_id" in asset.keys():
        clip_ids.append(asset["clip_id"])

total_duration = timedelta()
projects = []
for clip_id in clip_ids:
    metadata = FlowMetadata.getClipData(clip_id)
    if "error" in metadata.keys():
        continue
    if not metadata["has_video"]:
        continue
    
    asset_id = metadata["asset"]["asset_id"]
    new_metadata = metadata["asset"]
    try:
        if metadata["status_text"] == "Archived":
            path = metadata["video"][0]["file"]["archive_locations"][0]["userpath"]
            #pprint(metadata["video"][0]["file"]["archive_locations"][0]["userpath"])
        else:
            path = metadata["video"][0]["file"]["locations"][0]["userpath"]
            #pprint(metadata["video"][0]["file"]["locations"][0]["userpath"])
    except KeyError:
        continue
    
#     if "proxy" in path.lower():
#         continue
#     if "b-roll" in path.lower() or "b_roll" in path.lower() or "broll" in path.lower():
#         new_metadata["custom"][field["101a Genre German"]] = "B-Roll"
#     elif "itv" in path.lower() or "interview" in path.lower() in path.lower():
#         new_metadata["custom"][field["101a Genre German"]] = "Interview"
#     else:
#         try:
#             test = metadata["assets"]["custom"][field["101a Genre German"]]
#         except:
#             new_metadata["custom"][field["101a Genre German"]] = "Unknown"
#     new_metadata["custom"][field["104 Internal Notes"]] = path.split("/")[0]
#     data = json.dumps(new_metadata)
#     update = FlowMetadata.updateAsset(asset_id, data)
#     print(clip_id, update)

    # projects.append(path.split("/")[0])
    # print(list(set(projects)))

    # total_duration += calc_duration(metadata["video"][0]["timecode_duration"])
    # print(total_duration)


