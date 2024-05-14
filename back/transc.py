from youtube_transcript_api import YouTubeTranscriptApi as yta

def get_transcript(video_url):
    # Parse video ID from URL
    video_id = video_url.split('=')[-1]

    # Get transcript
    data = yta.get_transcript(video_id)

    # Extract text from transcript data
    transcript = ''
    for value in data:
        for key, val in value.items():
            if key == 'text':
                transcript += val + ' '

    # Join the lines and return the final transcript
    final_tra = " ".join(transcript.splitlines())
    
    return final_tra

