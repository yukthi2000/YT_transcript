from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import re 
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests

app = Flask(__name__)
CORS(app, support_credentials=True)

def extract_video_id(url):
    """Extracts the YouTube video ID from a URL."""
    # Regex to find video ID from various YouTube URL formats
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})(?:&.*)?$',
        # Short URLs
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]{11})(?:\?.*)?$',
        # Embed URLs
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})(?:\?.*)?$',
        # Old v= format
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([a-zA-Z0-9_-]{11})(?:\?.*)?$',
        # Playlist URLs
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/.*?list=.*?&v=([a-zA-Z0-9_-]{11})(?:&.*)?$',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/.*?v=([a-zA-Z0-9_-]{11})&list=',
        # Shorts URLs
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})(?:\?.*)?$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def check_video_availability(video_id):
    """Checks if the video is available."""
    response = requests.head(f"https://www.youtube.com/watch?v={video_id}")
    if response.status_code == 200:
        return True
    else:
        return False
    
def getVideodetails(url):
    ytt_api = YouTubeTranscriptApi()
    trans = ytt_api.fetch(url)
    language = trans.language
    generated= trans.is_generated
    return language, generated



        


@app.route('/link', methods=['POST','OPTIONS'])
# @cross_origin
def getlink():
    if request.method == 'OPTIONS':
        return '',200
    
    print("Request received")
    print("request data : ", request.data)

    data = request.get_json()

    if not data :
        print("No data received")
        return jsonify({"error": "No data received"}), 400
    

    url = data.get('link')
    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400
    vidav= check_video_availability(video_id)
    if not vidav:
        return jsonify({"error": "Video is not available"}), 400
    lan,gen = getVideodetails(video_id)
    return jsonify({"video_id": video_id,"lan":lan,"gen" : gen}), 200



if __name__ == "__main__":
    app.run(debug=True, port=5000)

