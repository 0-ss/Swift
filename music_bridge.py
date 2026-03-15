import gettext
gettext.translation = lambda *args, **kwargs: gettext.NullTranslations()
import sys
import json
import re
from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL

# Initialize YTMusic
yt = YTMusic()

def upgrade_thumb_quality(url):
    """
    Forces YouTube thumbnails to high resolution (800x800).
    Replaces =w120-h120 or =s90 type parameters with high-res equivalents.
    """
    if not url:
        return "https://i.imgur.com/tskAGyt.png"
    # Replace any existing size parameters with 800px high-res settings
    url = re.sub(r'=w\d+-h\d+.*', '=w800-h800-l90-rj', url)
    url = re.sub(r'=s\d+.*', '=s800', url)
    return url

def parse_duration_to_seconds(d):
    if d is None: return 0
    if isinstance(d, (int, float)): return int(d)
    s = str(d).strip()
    if not s or not ":" in s:
        return int(s) if s.isdigit() else 0
    parts = s.split(":")
    nums = [int(p) for p in parts if p.isdigit()]
    if len(nums) == 2: return nums[0]*60 + nums[1]
    if len(nums) == 3: return nums[0]*3600 + nums[1]*60 + nums[2]
    return 0

def search(query):
    try:
        # Use a general search first to find the "Top Result" and relevant matches
        search_results = yt.search(query)
        combined_results = []

        for r in search_results:
            result_type = r.get("resultType")
            
            # Process Tracks and Videos
            if result_type in ["song", "video"]:
                artists = r.get("artists", [])
                artist_name = ", ".join([a.get("name") for a in artists]) if artists else "Unknown Artist"
                album = r.get("album")
                album_name = album.get("name") if album else "YouTube Music"
                
                raw_thumb = r.get("thumbnails", [{}])[-1].get("url")
                
                combined_results.append({
                    "id": r.get("videoId"),
                    "title": r.get("title"),
                    "artistName": artist_name,
                    "albumTitle": album_name,
                    "duration": r.get("duration_seconds") or parse_duration_to_seconds(r.get("duration")),
                    "artwork": upgrade_thumb_quality(raw_thumb),
                    "source": "youtube",
                    "type": "track"
                })

            # Process Artists 
            elif result_type == "artist":
                raw_thumb = r.get("thumbnails", [{}])[-1].get("url")
                combined_results.append({
                    "id": r.get("browseId"),
                    "title": r.get("artist") or r.get("title"),
                    "artistName": "Artist",
                    "albumTitle": "",
                    "duration": 0,
                    "artwork": upgrade_thumb_quality(raw_thumb),
                    "source": "youtube",
                    "type": "artist"
                })

        return combined_results
    except Exception as e:
        return {"error": str(e)}

def get_stream(video_id):
    if not video_id: return {"error": "No ID"}
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "extractor_args": {"youtube": {"player_client": ["android", "web_music"]}},
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return {"url": info['url']}
    except Exception as e:
        return {"error": str(e)}

def get_duration(video_id):
    try:
        with YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return {"duration": int(info.get("duration") or 0)}
    except:
        return {"duration": 0}

if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 3: sys.exit(1)
    
    cmd, arg = sys.argv[1], sys.argv[2]
    if cmd == "search": print(json.dumps(search(arg)))
    elif cmd == "stream": print(json.dumps(get_stream(arg)))
    elif cmd == "duration": print(json.dumps(get_duration(arg)))