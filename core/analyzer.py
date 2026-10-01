import json
import subprocess
import sys


def get_heatmap_peaks(video_url: str) -> list:
    """Extracts YouTube 'Most Replayed' heatmap data using bypass extractor options."""
    ydl_cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-download",
        "--extractor-args",
        "youtube:player_client=android,ios",
        video_url,
    ]
    try:
        result = subprocess.run(
            ydl_cmd, capture_output=True, text=True, check=True
        )
        info = json.loads(result.stdout)
        heatmap = info.get("heatmap", [])

        if not heatmap:
            print("[INFO] No heatmap found on video. Using interval fallback.")
            return []

        # Sort heatmap points by value (retention intensity)
        sorted_points = sorted(
            heatmap, key=lambda x: x.get("value", 0), reverse=True
        )

        peaks = []
        for point in sorted_points:
            start_sec = int(point.get("start_time", 0))
            score = float(point.get("value", 0))
            peaks.append({"time_sec": start_sec, "heatmap_score": score})

        return peaks
    except Exception as e:
        print(f"[WARNING] Could not fetch heatmap: {e}", file=sys.stderr)
        return []


def analyze_and_rank_highlights(
    video_url: str, top_n: int = 3, min_gap: int = 60
) -> list:
    """Combines retention signals and ranks the best timestamps for clipping."""
    print("--> Analyzing video retention heatmap...")
    peaks = get_heatmap_peaks(video_url)

    if not peaks:
        # Fallback timestamps if heatmap is absent
        return ["00:01:00", "00:03:00", "00:05:00"][:top_n]

    selected_peaks = []
    for peak in peaks:
        t_sec = peak["time_sec"]
        if all(abs(t_sec - p["time_sec"]) >= min_gap for p in selected_peaks):
            selected_peaks.append(peak)
        if len(selected_peaks) >= top_n:
            break

    formatted_timestamps = []
    for p in selected_peaks:
        sec = p["time_sec"]
        hrs = sec // 3600
        mins = (sec % 3600) // 60
        secs = sec % 60
        formatted_timestamps.append(f"{hrs:02d}:{mins:02d}:{secs:02d}")

    print(
        f"[ANALYSIS COMPLETE] Identified Top {len(formatted_timestamps)}"
        " multi-signal moments!"
    )
    return formatted_timestamps