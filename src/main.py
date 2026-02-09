import pandas as pd
from src.youtube_client import get_youtube_client, get_videos_metadata
from src.playlist import get_video_ids_from_playlist

PLAYLISTS = [
    "PLRsbF2sD7JVpZ3O01elefwrp9l4yBWoXu",
    "PLGVZCDnMOq0qFokF2chnzTq4VtIcFXG5P"
]

def chunk_list(lst, size=50):
    for i in range(0, len(lst), size):
        yield lst[i:i+size]

def main():
    youtube = get_youtube_client()
    all_rows = []

    for playlist_id in PLAYLISTS:
        video_ids = get_video_ids_from_playlist(youtube, playlist_id)

        for chunk in chunk_list(video_ids):
            videos = get_videos_metadata(youtube, chunk)

            for v in videos:
                row = {
                    "video_id": v["id"],
                    "title": v["snippet"]["title"],
                    "description": v["snippet"]["description"],
                    "published_at": v["snippet"]["publishedAt"],
                    "views": int(v["statistics"].get("viewCount", 0)),
                    "likes": int(v["statistics"].get("likeCount", 0)),
                    "playlist_id": playlist_id
                }
                all_rows.append(row)

    df = pd.DataFrame(all_rows)
    df.to_csv("data/raw_videos.csv", index=False)

if __name__ == "__main__":
    main()
