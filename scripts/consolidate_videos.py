#!/usr/bin/env python3
"""
Consolidates all rendered scene videos into one final video.
Usage: python3 scripts/consolidate_videos.py
"""
import os
import subprocess
import glob
from pathlib import Path

def main():
    # Paths
    base_dir = Path(__file__).parent.parent
    media_dir = base_dir / "workspace" / "media"
    videos_dir = media_dir / "videos"
    output_file = media_dir / "final_video.mp4"
    
    # Find all rendered mp4 files
    pattern = str(videos_dir / "scene_*" / "720p30" / "*.mp4")
    video_files = sorted(glob.glob(pattern))
    
    if not video_files:
        print(f"No video files found matching: {pattern}")
        return
    
    print(f"Found {len(video_files)} video file(s):")
    for vf in video_files:
        print(f"  - {Path(vf).relative_to(base_dir)}")
    
    # Create temporary file list for ffmpeg concat demuxer
    concat_list = media_dir / "concat_list.txt"
    
    with open(concat_list, 'w') as f:
        for video_file in video_files:
            # ffmpeg concat demuxer requires absolute paths and 'file' prefix
            f.write(f"file '{os.path.abspath(video_file)}'\n")
    
    # Run ffmpeg to concatenate
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        "-y",  # Overwrite output file if exists
        str(output_file)
    ]
    
    print(f"\nConcatenating videos into: {output_file.relative_to(base_dir)}")
    print(f"Running: {' '.join(cmd)}\n")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n✓ Final video created: {output_file}")
        print(f"  Size: {output_file.stat().st_size / (1024*1024):.2f} MB")
        
        # Clean up temp file
        concat_list.unlink()
        
    except subprocess.CalledProcessError as e:
        print(f"✗ ffmpeg failed: {e}")
        raise
    except FileNotFoundError:
        print("✗ ffmpeg not found. Install it with: sudo apt install ffmpeg")
        raise

if __name__ == "__main__":
    main()
