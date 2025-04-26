import re

def shift_timecode(timecode, shift_seconds):
    hours, minutes, seconds_millis = timecode.split(":")
    seconds, millis = seconds_millis.split(",")
    
    total_millis = (int(hours) * 3600 + int(minutes) * 60 + int(seconds)) * 1000 + int(millis)
    total_millis += shift_seconds * 1000

    if total_millis < 0:
        total_millis = 0  # Prevent negative timestamps

    hours = total_millis // 3600000
    minutes = (total_millis % 3600000) // 60000
    seconds = (total_millis % 60000) // 1000
    millis = total_millis % 1000

    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

def shift_srt(input_file, output_file, shift_seconds):
    with open(input_file, 'r', encoding='cp1250') as f:
        content = f.read()

    def replace_timecodes(match):
        start = shift_timecode(match.group(1), shift_seconds)
        end = shift_timecode(match.group(2), shift_seconds)
        return f"{start} --> {end}"

    shifted_content = re.sub(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", replace_timecodes, content)

    with open(output_file, 'w', encoding='cp1250') as f:
        f.write(shifted_content)

# === SETTINGS ===
input_srt = "Ichi.The.Killer.2001.1080p.BluRay.x264-[YTS.AM].srt"   # << your file here
output_srt = "your_shifted.srt"   # << output file
shift_by_seconds = 66            # << shift by 66 seconds (1:54)

shift_srt(input_srt, output_srt, shift_by_seconds)

print("Done! Your new .srt file is ready.")
