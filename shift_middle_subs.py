import re
from datetime import timedelta

# Settings
input_file = "input.srt"       # your original subtitle file
output_file = "output.srt"     # the shifted subtitle file
encoding = "windows-1250"      # because your subtitles aren't utf-8
threshold_time = timedelta(minutes=1, seconds=54)  # Start shifting after 1:54
shift_seconds = 0              # no shift before threshold
shift_after_seconds = 114      # move everything after 1:54 by +114 seconds

def parse_timestamp(ts):
    hours, minutes, seconds_millis = ts.split(':')
    seconds, millis = seconds_millis.split(',')
    return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=int(millis))

def format_timestamp(td):
    total_seconds = int(td.total_seconds())
    millis = int(td.microseconds / 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

def shift_time(original_time):
    if original_time >= threshold_time:
        return original_time + timedelta(seconds=shift_after_seconds)
    else:
        return original_time + timedelta(seconds=shift_seconds)

with open(input_file, 'r', encoding=encoding) as f:
    content = f.read()

pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")

def shift_match(match):
    start = parse_timestamp(match.group(1))
    end = parse_timestamp(match.group(2))
    new_start = shift_time(start)
    new_end = shift_time(end)
    return f"{format_timestamp(new_start)} --> {format_timestamp(new_end)}"

new_content = pattern.sub(shift_match, content)

with open(output_file, 'w', encoding=encoding) as f:
    f.write(new_content)

print("✅ Done vole! Subtitles shifted successfully. Mas to hotovy.")