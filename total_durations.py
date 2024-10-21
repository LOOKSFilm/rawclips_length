from EditShareAPI import EsAuth, FlowMetadata, FlowSearch
import json
from timecode import Timecode
from datetime import datetime, timedelta

EsAuth.login("10.0.77.13", "christoph", "looksfilm")

field = FlowMetadata.getCustomMetadataFields().fields_dict

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours < 10:
        return f"{hours}:{minutes:02}:{seconds:02}"
    elif hours < 100:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    elif hours < 1000:
        return f"{hours:03}:{minutes:02}:{seconds:02}"
    else:
        return f"{hours:04}:{minutes:02}:{seconds:02}"

def pprint(data):
    print(json.dumps(data, indent=4))

# for item in FlowSearch.searchList():
#     print(item["fixed_field"])

def calc_duration(duration):
    hours, minutes, seconds, frames, str_fps = map(str, str(duration).split(":"))
    fps = float(str_fps.split("/")[0]) / float(str_fps.split("/")[1])
    seconds = float(seconds)
    seconds += float(frames) / float(fps)
    total_seconds = float(hours) * 3600 + float(minutes) * 60 + float(seconds)
    time_delta = timedelta(seconds=total_seconds)
    return time_delta

def get_broll_duration():
    search = [
        FlowSearch.createFilter("MEDIA_SPACES_NAMES", FlowSearch.GROUP_FILES, FlowSearch.MATCH_IS, "OCF OAF"),
        FlowSearch.createFilter(field["101a Genre German"], FlowSearch.GROUP_ASSETS, FlowSearch.MATCH_IS, "B-Roll")
        ]
    result = FlowSearch.searchAdvanced(FlowSearch.COMBINE_ALL, search)
    print(len(result))

    project_total_duration = dict()
    total_duration = timedelta()
    for clip in result:
        if "clip_id" in clip.keys():
            metadata = FlowMetadata.getClipData(clip["clip_id"])
            try:
                project = metadata["asset"]["custom"][field["104 Internal Notes"]]
                duration = calc_duration(metadata["video"][0]["timecode_duration"])
                if project in project_total_duration:
                    project_total_duration[project] += duration
                    total_duration += duration
                else:
                    project_total_duration[project] = duration
            except:
                continue
    project_total_duration["total"] = total_duration
    duration_dict = {key: str(format_timedelta(value)) for key, value in project_total_duration.items()}
    return duration_dict

def get_itv_duration():
    search = [
        FlowSearch.createFilter("MEDIA_SPACES_NAMES", FlowSearch.GROUP_FILES, FlowSearch.MATCH_IS, "OCF OAF"),
        FlowSearch.createFilter(field["101a Genre German"], FlowSearch.GROUP_ASSETS, FlowSearch.MATCH_IS, "Interview")
        ]
    result = FlowSearch.searchAdvanced(FlowSearch.COMBINE_ALL, search)
    print(len(result))

    project_total_duration = dict()
    total_duration = timedelta()
    for clip in result:
        if "clip_id" in clip.keys():
            metadata = FlowMetadata.getClipData(clip["clip_id"])
            try:
                project = metadata["asset"]["custom"][field["104 Internal Notes"]]
                duration = calc_duration(metadata["video"][0]["timecode_duration"])
                if project in project_total_duration:
                    project_total_duration[project] += duration
                    total_duration += duration
                else:
                    project_total_duration[project] = duration
            except:
                continue
    project_total_duration["total"] = total_duration
    duration_dict = {key: str(format_timedelta(value)) for key, value in project_total_duration.items()}
    return duration_dict

def get_unknown_duration():
    search = [
        FlowSearch.createFilter("MEDIA_SPACES_NAMES", FlowSearch.GROUP_FILES, FlowSearch.MATCH_IS, "OCF OAF"),
        FlowSearch.createFilter(field["101a Genre German"], FlowSearch.GROUP_ASSETS, FlowSearch.MATCH_IS, "Unknown")
        ]
    result = FlowSearch.searchAdvanced(FlowSearch.COMBINE_ALL, search)
    print(len(result))

    project_total_duration = dict()
    total_duration = timedelta()
    for clip in result:
        if "clip_id" in clip.keys():
            metadata = FlowMetadata.getClipData(clip["clip_id"])
            try:
                project = metadata["asset"]["custom"][field["104 Internal Notes"]]
                duration = calc_duration(metadata["video"][0]["timecode_duration"])
                if project in project_total_duration:
                    project_total_duration[project] += duration
                    total_duration += duration
                else:
                    project_total_duration[project] = duration
            except:
                continue
    project_total_duration["total"] = total_duration
    duration_dict = {key: str(format_timedelta(value)) for key, value in project_total_duration.items()}
    return duration_dict

def get_drama_duration():
    search = [
        FlowSearch.createFilter("MEDIA_SPACES_NAMES", FlowSearch.GROUP_FILES, FlowSearch.MATCH_IS, "OCF OAF"),
        FlowSearch.createFilter(field["101a Genre German"], FlowSearch.GROUP_ASSETS, FlowSearch.MATCH_IS, "Drama")
        ]
    result = FlowSearch.searchAdvanced(FlowSearch.COMBINE_ALL, search)
    print(len(result))

    project_total_duration = dict()
    total_duration = timedelta()
    for clip in result:
        if "clip_id" in clip.keys():
            metadata = FlowMetadata.getClipData(clip["clip_id"])
            try:
                project = metadata["asset"]["custom"][field["104 Internal Notes"]]
                duration = calc_duration(metadata["video"][0]["timecode_duration"])
                if project in project_total_duration:
                    project_total_duration[project] += duration
                    total_duration += duration
                else:
                    project_total_duration[project] = duration
            except:
                continue
    project_total_duration["total"] = total_duration
    duration_dict = {key: str(format_timedelta(value)) for key, value in project_total_duration.items()}
    return duration_dict

broll = get_broll_duration()
with open("b-roll_durations.json", "w") as f:
    json.dump(broll, f, indent=4)

interview = get_itv_duration()
with open("interview_durations.json", "w") as f:
    json.dump(interview, f, indent=4)

drama = get_drama_duration()
with open("drama_durations.json", "w") as f:
    json.dump(drama, f, indent=4)

unknown = get_unknown_duration()
with open("unknown_durations.json", "w") as f:
    json.dump(unknown, f, indent=4)


