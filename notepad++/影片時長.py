import requests
from bs4 import BeautifulSoup
import re

# YouTube video URL
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Send a GET request to the video URL
response = requests.get(video_url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the element containing the video duration
duration_element = soup.find("span", {"class": "ytp-time-duration"})

# Extract the duration text from the element
duration_text = duration_element.get_text()

# Convert the duration from "mm:ss" format to seconds
minutes, seconds = map(int, duration_text.split(":"))
duration_seconds = minutes * 60 + seconds

print("Video duration:", duration_seconds, "seconds")
