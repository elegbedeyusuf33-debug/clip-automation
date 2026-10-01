# 🎬 AI-Powered Short-Form Video Automation Pipeline

An automated Python pipeline that extracts viral moments from long-form YouTube videos, crops them into 9:16 vertical video formats, generates offline speech-to-text subtitles, and merges them into engaging, short-form compilations for TikTok, YouTube Shorts, and Instagram Reels.

---

## 🚀 Key Features

* **Data-Efficient Stream Processing:** Extracts raw video streams via `yt-dlp` on-the-fly without downloading entire long VODs locally.
* **Multi-Signal Moment Scoring:** Uses YouTube audience retention heatmaps (`yt-dlp` metadata extraction) to identify peak viewer engagement spikes.
* **FFmpeg Hardware-Accelerated Rendering:** Handles 16:9 to 9:16 vertical cropping, concatenation, and dual-feed split-screen layout generation.
* **Offline AI Transcriptions:** Integrated with OpenAI Whisper to transcribe audio locally on CPU (`FP32` fallback) and generate timed `.srt` dynamic captions.
* **Automatic Subtitle Burning:** Uses FFmpeg filtergraphs to burn styled, high-contrast captions directly onto vertical videos.
* **Dual-Feed Split-Screen Support:** Optional `--split` mode for gaming/reaction streams (webcam feed on top, gameplay on bottom).

---

## 📁 System Architecture

```text
clip-automation/
│
├── core/
│   ├── analyzer.py      # Heatmap extraction & retention peak ranking
│   ├── downloader.py    # Direct stream URL fetching via yt-dlp
│   ├── processor.py     # FFmpeg vertical cropping, split-screen, & clip merging
│   └── subtitles.py     # OpenAI Whisper transcription & SRT caption burning
│
├── output/              # Target folder for generated compilations
├── main.py              # CLI entry point & workflow coordinator
├── requirements.txt     # Python dependencies
└── README.md            # Documentation