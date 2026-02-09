from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

def get_youtube_client():
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing YOUTUBE_API_KEY")

    return build(
        "youtube",
        "v3",
        developerKey=api_key
    )

def get_videos_metadata(youtube, video_ids):
    request = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    )
    response = request.execute()
    return response["items"]
