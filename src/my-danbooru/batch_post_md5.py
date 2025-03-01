import hashlib
import json
import os
import sys
import requests
import cv2
from PIL import Image
import io

class RequestError(Exception):
    def __init__(self, status_code, response_data):
        super().__init__(f"Error: Received status code {status_code}")
        self.status_code = status_code
        self.response_data = response_data
class File:
    def __init__(self, file_path):
        self.file = open(file_path, 'rb')
        md5_hash = hashlib.md5()
        for chunk in iter(lambda: self.file.read(4096), b""):
            md5_hash.update(chunk)
        self.hash = md5_hash.hexdigest()
    def read(self):
        self.file.seek(0)
        return self.file
    def close(self):
        self.file.close()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
def get_mp4_last_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise ValueError("Could not read video file")
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    last_frame = Image.fromarray(frame_rgb)
    return img_to_buffer(last_frame)
def get_gif_last_frame(gif_path):
    with Image.open(gif_path) as img:
        img.seek(img.n_frames - 1)
        last_frame = img.copy()
    return img_to_buffer(last_frame)
def img_to_buffer(img):
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

def fetchBooru():
    response = requests.get(uploadUrl)
    uploads_md5_list = [
        asset["media_asset"]["md5"]
        for item in response.json()
        for asset in item["upload_media_assets"]
    ]
    response = requests.get(postUrl)
    posts_md5_list = [
        item["md5"] for item in response.json()
    ]
    return (uploads_md5_list, posts_md5_list)


def tag(path, file):
    frame = get_mp4_last_frame(path) if path.endswith('.mp4') else get_gif_last_frame(path) if path.endswith('.gif') else None
    files = {
        'file': (path, frame or file)
    }
    response = requests.post(wdTaggerUrl, params=wdParams, headers={'accept': 'application/json'}, files=files)
    res = response.json()
    if response.status_code != 200:
        raise RequestError(response.status_code, res)
    general_tags = response["general_res"]
    char_tags = response["character_res"]
    rating = response["rating"]
    rating = max(rating, key=rating.get)[0]
    char_tags = [k for k, _v in char_tags.items()] if len(char_tags) > 0 else ["unindentified_char"]
    print(f"\tRating: {rating} Character: {','.join(char_tags)} - {len(general_tags)}gen tags")
    return (general_tags, char_tags, rating)




apiKey = ""
user = ""
wdTaggerUrl = "http://127.0.0.1:5010/upload"
wdParams = {
    'general_threshold': 0.35,
    'character_threshold': 0.8
}
uploadUrl = f"http://localhost:3000/uploads.json?api_key={apiKey}&login={user}"
postUrl = f"http://localhost:3000/posts.json?api_key={apiKey}&login={user}"
addedListPath = "./my-danbooru-addedList.json"


def batchUpload(basePath):
    if not basePath: basePath = input("Base Path: ")
    batchTag = input("Batch Tag: ") or []
    if batchTag != []: batchTag = batchTag.split(" ")


# def checkReupload(up, po):
#     for i in range(len(up)):
#         if not up[i] in po:



def main():
    up, po = fetchBooru()
    print(up, po)
main()