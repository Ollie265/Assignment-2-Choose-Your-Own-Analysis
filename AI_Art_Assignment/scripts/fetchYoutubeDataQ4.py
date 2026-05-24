import json
import sys
from youtubeClient import youtubeClient


def fetchYoutubeData(searchQuery, maxVideos=25, maxCommentsPerVideo=50, outputFile='youtubeDataDump.json'):
    """
    Fetch YouTube videos and their comments, then save to a JSON file.

    @param searchQuery: search query string (e.g. 'RMIT University')
    @param maxVideos: maximum number of videos to retrieve
    @param maxCommentsPerVideo: maximum number of comments per video
    @param outputFile: output JSON filename
    """

    client = youtubeClient()

    # Step 1: Search for videos
    print(f"Searching for videos with query: '{searchQuery}'...")
    searchResponse = client.search().list(
        q=searchQuery,
        part='snippet',
        type='video',
        order='viewCount',
        maxResults=min(maxVideos, 50)  # YouTube API max per request is 50
    ).execute()

    videoIds = []
    videoSnippets = {}
    for item in searchResponse.get('items', []):
        videoId = item['id']['videoId']
        videoIds.append(videoId)
        videoSnippets[videoId] = item['snippet']

    print(f"  Found {len(videoIds)} videos.")

    # Step 2: Get video statistics (viewCount, likeCount)
    print("Fetching video statistics...")
    statsResponse = client.videos().list(
        id=','.join(videoIds),
        part='statistics'
    ).execute()

    videoStats = {}
    for item in statsResponse.get('items', []):
        videoStats[item['id']] = item['statistics']

    # Step 3: Get comments for each video
    print("Fetching comments...")
    videos = []

    for videoId in videoIds:
        snippet = videoSnippets[videoId]
        stats = videoStats.get(videoId, {})

        video = {
            'title': snippet['title'],
            'videoId': videoId,
            'channelTitle': snippet['channelTitle'],
            'publishedAt': snippet['publishedAt'],
            'viewCount': int(stats.get('viewCount', 0)),
            'likeCount': int(stats.get('likeCount', 0)),
            'comments': []
        }

        try:
            commentResponse = client.commentThreads().list(
                videoId=videoId,
                part='snippet',
                maxResults=maxCommentsPerVideo,
                textFormat='plainText'
            ).execute()

            for commentThread in commentResponse.get('items', []):
                topComment = commentThread['snippet']['topLevelComment']['snippet']
                video['comments'].append({
                    'author': topComment['authorDisplayName'],
                    'text': topComment['textDisplay'],
                    'publishedAt': topComment['publishedAt'],
                    'likeCount': topComment.get('likeCount', 0)
                })

            print(f"  {snippet['title'][:50]}... → {len(video['comments'])} comments")

        except Exception as e:
            print(f"  {snippet['title'][:50]}... → Comments disabled or error: {e}")

        videos.append(video)

    # Step 4: Save to JSON
    data = {'videos': videos}
    with open(outputFile, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Saved {len(videos)} videos to '{outputFile}'.")


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':

    QUERIES = [
        'AI art creative process',
        'AI art creativity',
        'AI art skill',
        'artists using AI art',
        'future of AI art',
        'AI tools for artists',
        'Midjourney art process',
        'does ai make art accessible',
        'AI art workflow',
        'Stable Diffusion art process'

    ]

    MAX_VIDEOS = 10
    MAX_COMMENTS = 100

    for query in QUERIES:
        safe_name = query.lower().replace(' ', '_').replace('/', '_').replace('?', '')
        output_file = f'../data/raw/{safe_name}_Q4.json'

        fetchYoutubeData(
            searchQuery=query,
            maxVideos=MAX_VIDEOS,
            maxCommentsPerVideo=MAX_COMMENTS,
            outputFile=output_file
        )
