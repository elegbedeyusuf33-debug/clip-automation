import sys
import yt_dlp


def get_stream_url(video_url: str) -> str:
    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "quiet": True,
        "no_warnings": True,
        # Uses Android / iOS player clients to bypass JS challenge requirements
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "ios"],
            }
        },
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            # If top-level 'url' exists, return it
            if "url" in info:
                return info["url"]

            # Otherwise, search requested formats for a working direct stream link
            if "requested_formats" in info:
                for fmt in info["requested_formats"]:
                    if fmt.get("vcodec") != "none" and "url" in fmt:
                        return fmt["url"]

            # Fallback to the top format entry with a valid URL
            if "formats" in info:
                for fmt in reversed(info["formats"]):
                    if fmt.get("url"):
                        return fmt["url"]

            raise KeyError("Could not extract a valid stream URL from media info.")

    except Exception as e:
        print(f"[ERROR] Failed to fetch stream URL: {e}", file=sys.stderr)
        raise