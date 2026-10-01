import argparse
import os
from core.analyzer import analyze_and_rank_highlights
from core.downloader import get_stream_url
from core.processor import merge_clips, process_clip
from core.subtitles import burn_subtitles_to_video, generate_subtitles


def main():
    parser = argparse.ArgumentParser(
        description="Automated Viral Short & Clip Pipeline"
    )
    parser.add_argument(
        "--url", required=True, help="Target YouTube or video URL"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=20,
        help="Duration per clip segment in seconds (default: 20)",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Automatically detect best moments via multi-signal analysis",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=3,
        help="Number of auto clips to generate (default: 3)",
    )
    parser.add_argument(
        "--split",
        action="store_true",
        help="Enable dual-feed split-screen layout (top: webcam/reaction, bottom: gameplay)",
    )

    args = parser.parse_args()

    os.makedirs("output", exist_ok=True)

    if args.auto:
        print("--> Starting Multi-Signal Highlight Detection...")
        highlights = analyze_and_rank_highlights(args.url, top_n=args.count)

        print("--> Extracting media stream URL...")
        stream_url = get_stream_url(args.url)

        generated_clips = []

        for index, start_time in enumerate(highlights, 1):
            out_filename = f"part_{index}.mp4"
            destination = os.path.join("output", out_filename)

            print(
                f"\n[Processing Top Moment {index}/{len(highlights)}]"
                f" Timestamp: {start_time}"
            )
            process_clip(
                stream_url,
                start_time=start_time,
                duration=args.duration,
                output_path=destination,
                split_screen=args.split,
            )
            generated_clips.append(destination)

        raw_compilation = os.path.join("output", "temp_raw_compilation.mp4")
        final_reel_path = os.path.join("output", "final_compilation.mp4")

        print("\n--> Merging peak moments into compilation...")
        merge_clips(generated_clips, raw_compilation)

        srt_file = generate_subtitles(raw_compilation)
        burn_subtitles_to_video(raw_compilation, srt_file, final_reel_path)

        # Cleanup temporary files
        for clip in generated_clips + [raw_compilation, srt_file]:
            if os.path.exists(clip):
                os.remove(clip)

        print("\n🎉 Pipeline Complete! Captioned compilation saved in /output!")


if __name__ == "__main__":
    main()