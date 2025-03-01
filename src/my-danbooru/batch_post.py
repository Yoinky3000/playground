import hashlib
import json
import os
import sys
import requests
import cv2
from PIL import Image
import io

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

def load_items_from_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return set(json.load(f))
    return set()  # Return an empty list if the file does not exist

def save_item_to_json(file_path, content):
    """Append the item to the JSON file."""
    with open(file_path, 'w') as f:
        json.dump(list(content), f)

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
        # Seek to the last frame
        img.seek(img.n_frames - 1)
        last_frame = img.copy()  # Make a copy of the last frame
    return img_to_buffer(last_frame)

def img_to_buffer(img):
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')  # You can change format if needed
    buffer.seek(0)
    return buffer

def calcMD5(path):
    md5_hash = hashlib.md5()
    with open(path, 'rb') as file:
        # Read and update the hash string in blocks
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()






def upload(basePath, batchTag):
    def progressPrint(msg, current, edit=False):
        sys.stdout.write('\033[K')
        print(f"{current}/{totalItems}: {msg}", end='\r' if edit else '\n')


    if batchTag != []:
        batchTag = batchTag.split(" ")

    addedList = load_items_from_json(addedListPath)

    items = os.listdir(basePath)

    totalItems = len(items)

    print(f"Detected {totalItems} files")

    succeed = 0
    skip = 0
    dir = 0

    for i in range(totalItems):
        item = items[i]
        full_path = os.path.join(basePath, item)
        if os.path.isdir(full_path):
            if input(f"{item} is a directory, ignore? ") == "Y":
                skip+=1
                progressPrint(f"{item} is a directory, ignoring", i+1)
            else:
                print("\n\n")
                batchTag = input(f"Batch Tag for {full_path}: ") or []
                addedList.update(upload(full_path, batchTag))
                dir+=1
                print("\n\n")
            continue

        md5 = calcMD5(full_path)
        if md5 in addedList:
            skip+=1
            progressPrint(f"{item} was added, ignoring", i+1)
            continue
        
        progressPrint(f"{item} > requesting result from tagger...", i+1, edit=True)

        frame = get_mp4_last_frame(full_path) if item.endswith('.mp4') else get_gif_last_frame(full_path) if item.endswith('.gif') else None
        files = {
            'file': (full_path, frame or open(full_path, 'rb'))
        }
        response = requests.post(wdTaggerUrl, params=wdParams, headers={'accept': 'application/json'}, files=files)
        if response.status_code != 200:
            progressPrint(f"{item} > error when requesting tagger, skipping...", i+1)
            print(response.json())
            continue
        response = response.json()
        general_tags = response["general_res"]
        char_tags = response["character_res"]
        rating = response["rating"]
        rating = max(rating, key=rating.get)[0]
        possibleChar = [key for key, value in char_tags.items() if value > 0.5] if len(char_tags) > 0 else ["unidentified_char"]
        progressPrint(f"{item} > Result - {', '.join(possibleChar)} ({len(general_tags)} gen tags) r:{rating}, uploading to my-danbooru...", i+1, edit=True)

        possibleChar = [f"char:{char}" for char in possibleChar]
        general_tags = list(general_tags.keys())
        tags = [s.replace(" ", "_") for s in possibleChar + general_tags + batchTag]
        if frame: tags.append("video")
        files = [
            ("upload[files][0]", open(full_path, 'rb')),
        ]
        response = requests.post(uploadUrl, files=files)
        if response.status_code != 201:
            progressPrint(f"{item} > error when uploading, skipping...", i+1)
            print(response.json())
            continue
        response = response.json()
        uploadId = response["id"]
        progressPrint(f"[r:{rating} {len(tags)}t]{item} > uploaded #{uploadId}, posting to my-danbooru...", i+1, edit=True)

        data = {
            'upload_media_asset_id': uploadId,
            'tag_string': " ".join(tags),
            'rating': rating,
        }
        response = requests.post(postUrl, json=data, headers={'accept': 'application/json'})
        if response.status_code == 200:
            succeed = 0
            progressPrint(f"[u#{uploadId} r:{rating} {len(tags)}t]{item} > already posted", i+1)
            addedList.add(md5)
            save_item_to_json(addedListPath, addedList)
            continue
        if response.status_code != 201:
            progressPrint(f"[u#{uploadId} r:{rating} {len(tags)}t]{item} > error when posting", i+1)
            print(response)
            continue
        response = response.json()
        postId = response["id"]
        progressPrint(f"[u#{uploadId} r:{rating} {len(tags)}t]{item} > posted #{postId}", i+1)

        addedList.add(md5)
        save_item_to_json(addedListPath, addedList)

        succeed+=1

    save_item_to_json(addedListPath, addedList)
    print(f"Succeed: {succeed} Skipped: {skip} Directory: {dir} Total: {succeed+skip+dir}/{totalItems}")
    return addedList


basePath = input("Base Path: ")
batchTag = input("Batch Tag: ") or []
upload(basePath, batchTag)