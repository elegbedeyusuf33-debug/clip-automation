import os
import subprocess
import whisper


def generate_subtitles(video_path: str, output_srt: str = "temp_subs.srt"):
    """Transcribes video audio using Whisper and generates an SRT subtitle file."""
    print("--> Transcribing audio with OpenAI Whisper (this takes a few seconds)...")
    model = whisper.load_model("base")
    result = model.transcribe(video_path)

    with open(output_srt, "w", encoding="utf-8") as f:
        for idx, segment in enumerate(result["segments"], 1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()

            f.write(f"{idx}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")

    return output_srt


def format_timestamp(seconds: float) -> str:
    """Converts seconds into SRT timecode format (HH:MM:SS,mmm)."""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"


def burn_subtitles_to_video(video_path: str, srt_path: str, output_path: str):
    """Uses FFmpeg to burn bold, centered social-media styled captions onto the video."""
    # Convert backslashes for FFmpeg pathing
    clean_srt = srt_path.replace("\\", "/").replace(":", "\\:")

    # Style: Bold Yellow Text with Black Outline in the Middle-Bottom Screen
    style = "Fontname=Arial,Fontsize=14,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=30"

    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        video_path,
        "-vf",
        f"subtitles={clean_srt}:force_style='{style}'",
        "-c:a",
        "copy",
        "-y",
        output_path,
    ]

    subprocess.run(
        ffmpeg_cmd,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    print(f"✨ [SUBTITLES BURNED] Captioned clip saved to: {output_path}")