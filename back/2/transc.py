import moviepy.editor as mp
import speech_recognition as sr
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse

def get_transcript(video_url):
    try:
        # Parse video ID from URL
        video_id = urllib.parse.urlparse(video_url).query[2:]

        # Get transcript for the video
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine transcript text
        text = ""
        for segment in transcript:
            text += segment['text'] + " "

        return text.strip()

    except Exception as e:
        print("Error:", e)
        return None

