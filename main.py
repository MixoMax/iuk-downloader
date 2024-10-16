import sys
import requests
import subprocess
import bs4

url = sys.argv[1]

response = requests.get(url)

soup = bs4.BeautifulSoup(response.text, "html.parser")


# find all a tags
a_tags = soup.find_all("a")
links = []
for tag in a_tags:
    link = tag.get("href")
    if link:
        links.append(link)

# only keep links that contain "youtu" so all youtube.com / .de
youtube_links = [link for link in links if "youtu" in link]


# download all youtube links
for link in youtube_links:
    subprocess.run(["yt-dlp", link, "-o", "downloads/%(title)s.%(ext)s"])