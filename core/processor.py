import os
import subprocess


def process_clip(
    stream_url: str,
    start_time: str,
    duration: int,
    output_path: str,
    split_screen: bool = True,
):
    """Clips and processes video into a vertical 9:16 layout.

    Supports single center-crop or dual-feed facecam/gameplay split-screen.
    """
    if split_screen:
        # Complex filter graph:
        # 1. Takes top crop (facecam area) and resizes to upper 9:16 block
        # 2. Takes bottom-center crop (gameplay) and resizes to lower 9:16 block
        # 3. Stacks them vertically (vstack)
        filter_graph = (
            "[0:v]crop=iw:ih/2:0:0,scale=1080:960[top];"
            "[0:v]crop=ih*(9/16):ih/2:(iw-ih*(9/16))/2:ih/2,scale=1080:960[bottom];"
            "[top][bottom]vstack=inputs=2[v]"
        )
        video_map = "-map [v] -map 0:a?"
    else:
        # Standard single center crop
        filter_graph = "crop=ih*(9/16):ih"
        video_map = ""

    ffmpeg_cmd = [
        "ffmpeg",
        "-ss",
        start_time,
        "-i",
        stream_url,
        "-t",
        str(duration),
        "-vf" if not split_screen else "-filter_complex",
        filter_graph,
    ]

    if video_map:
        ffmpeg_cmd.extend(video_map.split())

    ffmpeg_cmd.extend(
        [
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-preset",
            "ultrafast",
            "-y",
            output_path,
        ]
    )

    try:
        subprocess.run(
            ffmpeg_cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        print(f"[SUCCESS] Clip generated: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] FFmpeg failed to process video: {e}")
        raise


def merge_clips(clip_paths: list, final_output_path: str):
    """Merges multiple MP4 video clips into a single compilation file."""
    concat_file = "temp_concat_list.txt"

    with open(concat_file, "w", encoding="utf-8") as f:
        for path in clip_paths:
            clean_path = path.replace("\\", "/")
            f.write(f"file '{clean_path}'\n")

    ffmpeg_cmd = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        concat_file,
        "-c",
        "copy",
        "-y",
        final_output_path,
    ]

    try:
        subprocess.run(
            ffmpeg_cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        print(
            f"\n🔥 [HIGHLIGHT REEL CREATED] Combined video saved to:"
            f" {final_output_path}"
        )
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to merge clips: {e}")
    finally:
        if os.path.exists(concat_file):
            os.remove(concat_file)