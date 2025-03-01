import hashlib
from multiprocessing.managers import ListProxy
import sys
import json
import os
from multiprocessing import Process, Queue, Pool, Manager
import math
import cv2
import requests
from PIL import Image
import io

DEFAULT = "DEFAULT"
LOG = "LOG"
DONE = "DONE"
SKIP = "A"
ERR = "B"
SUCCEED = "C"
# CHAR_TAGS = "D"
# GENERAL_TAGS = "E"
# RATING = "F"
class File:
    def __init__(self, file_path: str):
        self.path = file_path
        self.file = open(file_path, 'rb')
    def read(self):
        self.file.seek(0)
        return self.file
    def close(self):
        self.file.close()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

# JSON
# def load_items_from_json(file_path):
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as f:
#             return json.load(f)
#     return []
# def save_item_to_json(file_path, content):
#     with open(file_path, 'w') as f:
#         json.dump(list(content), f)


# FETCH BOORU POSTS MD5
def fetchPage(page):
    response = requests.get(postUrl(page)).json()
    return [item["md5"] for item in response]
def fetchBooru():
    response = requests.get(postUrl()).json()
    if len(response) == 0: return []
    pages = math.ceil(response[0]["id"] / len(response))
    with Pool(60) as p:
        result = p.map(fetchPage, [i + 1 for i in range(pages)])
        return [item for sublist in result for item in sublist]


# MULTI PROCESS LOGGER
def update_lines(log_lines, status, processes):
    processes += 1
    combined = log_lines + [""] + status
    num_lines = len(combined)
    if num_lines > processes:
        for i in range(num_lines - processes):
            print("")
    for i in range(num_lines):
        i = num_lines - i -1
        sys.stdout.write('\033[F')
        if i < num_lines - 1:
            sys.stdout.write('\033[F')
        sys.stdout.write('\033[K')
        print(combined[i])
    for i in range(num_lines-1):
        sys.stdout.write('\033[B')
def itemsLogHandler(processes, ev: Queue):
    result = {
        SUCCEED: 0,
        SKIP: 0,
        ERR: 0
    }
    done = 0
    status = ["Waiting"] * processes
    err_lines = []
    print("\n".join([""]+status))
    while done != processes:
        log_lines = []
        type, data = ev.get(block=True)
        if type == DONE:
            id = data
            log_lines.append(f"Process {id} is DONE")
            status[id] = f"Process {id} | All items are processed"
            done += 1
        elif type != ERR:
            id, msg, res = data
            if res: result[res] += 1
            msg = f"Process {id} | {msg}"
            if type == LOG:
                log_lines.append(msg)
            status[id] = msg
        else:
            err_lines.append(data)
        update_lines(log_lines, status, processes)
    print(f"Finished - {result[SUCCEED]} Succeed, {result[SKIP]} Skipped, {result[ERR]} Errored")
    for err in err_lines:
        print(err)


# Utils
def distributeItems(items, num):
    result = [[] for _ in range(num)]
    for index, element in enumerate(items):
        result[index % num].append(element)
    return result
def calcMD5(file):
    md5_hash = hashlib.md5()
    for chunk in iter(lambda: file.read(4096), b""):
        md5_hash.update(chunk)
    return md5_hash.hexdigest()
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
def itemsChecker(basePath, items, folders: ListProxy, files: ListProxy, repeated: ListProxy, seenList: ListProxy):
    for item in items:
        full_path = os.path.join(basePath, item)
        if os.path.isdir(full_path):
            folders.append(item)
        else:
            md5 = calcMD5(open(full_path, 'rb'))
            if md5 in seenList:
                repeated.append(item)
                continue
            
            seenList.append(md5)
            files.append({"item": item, "md5": md5})


# API
def tagger(id:int, batchTag, path: str, ev: Queue, item, i, ti):
    ev.put((DEFAULT, (id, f"[{i}/{ti}] [TAGGING] {item}", None)))
    frame = get_mp4_last_frame(path) if path.endswith('.mp4') else get_gif_last_frame(path) if path.endswith('.gif') else None
    files = {
        'file': (path, frame or open(path, 'rb'))
    }
    response = requests.post(wdTaggerUrl(id), params=wdParams, headers={'accept': 'application/json'}, files=files)
    if response.status_code != 200:
        ev.put((LOG, (id, f"[{i}/{ti}] [TAGGER ERROR] {item}", ERR)))
        res = response.json()
        res["file"] = path
        ev.put((ERR, res))
        return ERR
    response = response.json()
    general_tags = response["general_res"]
    char_tags = response["character_res"]
    rating = response["rating"]
    rating = max(rating, key=rating.get)[0]
    possibleChar = [key for key, value in char_tags.items() if value > 0.5] if len(char_tags) > 0 else ["unidentified_char"]
    ev.put((DEFAULT, (id, f"[{i}/{ti}] [UPLOADING] {item} tagger result - {', '.join(char_tags)} ({len(general_tags)} gen tags) r:{rating}", None)))
    possibleChar = [f"char:{char}" for char in possibleChar]
    general_tags = list(general_tags.keys())
    tags = [s.replace(" ", "_") for s in possibleChar + general_tags + batchTag]
    return (tags, rating)

def upload(id, file: File, ev: Queue, item, i, ti, retries = 0):
    files = [
        ("upload[files][0]", file.read()),
    ]
    response = requests.post(uploadUrl, files=files)
    if response.status_code != 201:
        if (retries <= 5):
            retries += 1
            ev.put((DEFAULT, (id, f"[{i}/{ti}] [UPLOAD RETRIES {retries}/5] {item} {response.status_code}", None)))
            return upload(id, file, ev, item, i, ti, retries)
        else:
            ev.put((LOG, (id, f"[{i}/{ti}] [UPLOAD ERROR] {item} {response.status_code}", ERR)))
            res = response.json()
            res["file"] = file.path
            ev.put((ERR, res))
            return ERR
    response = response.json()
    uploadId = response["id"]
    ev.put((DEFAULT, (id, f"[{i}/{ti}] [POSTING] {item} uploaded #{uploadId}", None)))
    return uploadId

def post(id, uploadId, tags, rating, ev: Queue, item, i, ti, fp, retries = 0):
    data = {
        'upload_media_asset_id': uploadId,
        'tag_string': " ".join(tags),
        'rating': rating,
    }
    response = requests.post(postUrl(), json=data, headers={'accept': 'application/json'})
    if response.status_code == 200:
        ev.put((LOG, (id, f"[{i}/{ti}] [POSTED ALREADY] {item}", SKIP)))
        return SKIP
    if response.status_code != 201:
        if (retries <= 5):
            retries += 1
            ev.put((DEFAULT, (id, f"[{i}/{ti}] [POST RETRIES {retries}/5] {item} {response.status_code}", None)))
            return post(id, uploadId, tags, rating, ev, item, i, ti, fp, retries)
        else:
            ev.put((LOG, (id, f"[{i}/{ti}] [POST ERROR] {item} {response.status_code}", ERR)))
            res = response.json()
            res["file"] = fp
            ev.put((ERR, res))
            return ERR
    response = response.json()
    postId = response["id"]
    ev.put((LOG, (id, f"[{i}/{ti}] [POSTED #{postId}] {item}", SUCCEED)))
    return SUCCEED


# MAIN
def itemsHandler(id, basePath, batchTag, addedList: ListProxy, items, ev: Queue):
    global testKey
    totalItems = len(items)
    for i in range(totalItems):
        item = items[i]
        path = item["item"]
        md5 = item["md5"]
        i+=1
        full_path = os.path.join(basePath, path)
        file = File(full_path)
        if os.path.isdir(full_path):
            ev.put((DEFAULT, (id, f"[{i}/{totalItems}]{path} is a directory, ignoring", SKIP)))
            continue
        if md5 in addedList:
            ev.put((DEFAULT, (id, f"[{i}/{totalItems}]{path} was added, ignoring", SKIP)))
            continue
        res = tagger(id, batchTag, full_path, ev, path, i, totalItems)
        if res == ERR: continue
        tags, rating = res
        res = upload(id, file, ev, path, i, totalItems)
        if res == ERR: continue
        uploadId = res
        res = post(id, uploadId, tags, rating, ev, path, i, totalItems, full_path)
        if res == SUCCEED: addedList.append(md5)
    ev.put((DONE, id))


def main(basePath, batchTag, addedList: ListProxy = None):
    if batchTag != []:
        batchTag = batchTag.split(" ")
    items = os.listdir(basePath)

    if not addedList:
        addedList = Manager().list()
        addedList.extend(fetchBooru())
    seenList = Manager().list()
    repeated = Manager().list()
    files = Manager().list()
    folders = Manager().list()

    distItems = distributeItems(items, len(items) if len(items) < 20 else 20)
    pList: list[Process] = []
    for di in distItems:
        p = Process(target=itemsChecker, args=(basePath, di, folders, files, repeated, seenList))
        pList.append(p)
        p.start()
    for p in pList:
        p.join()

    print(f"Total {len(folders)} folders")
    for folder in folders:
        full_path = os.path.join(basePath, folder)
        if input(f"{full_path} is a directory, ignore? ") == "Y":
            print(f"{full_path} is a directory, ignoring")
        else:
            print("\n\n")
            print(f"---- BEGIN {full_path} ----")
            currentBatchTag = " ".join(batchTag)
            newBatchTag = input(f"Batch Tag for {full_path} (current: {currentBatchTag}): ") or currentBatchTag
            main(full_path, newBatchTag, addedList)
            print(f"---- END {full_path} ----")
            print("\n\n")

    if (len(files) == 0): return
    for item in repeated:
        print(f"{item} was repeated, skipping")
    print(f"Total {len(files)} files")
    distItems = distributeItems(files, processes)
    ev = Queue()
    log_process = Process(target=itemsLogHandler, args=(processes, ev))
    log_process.start()
    pList = []
    for i in range(processes):
        p = Process(target=itemsHandler, args=(i, basePath, batchTag, addedList, distItems[i], ev))
        pList.append(p)
        p.start()
    for p in pList:
        p.join()







processes = 15
# addedListPath = "./my-danbooru-addedList.json"
prodKey = "pBY75Sg47hQLRpo3RaZ24BTQ"
testKey = "AnyQsEFRSWWg8p4aLGWDHeKS"
testKeyEmpty = ""
test = False
user = "yoinky"
def wdTaggerUrl(id):
    return f"http://127.0.0.1:501{id % 3}/upload"
wdParams = {
    'general_threshold': 0.35,
    'character_threshold': 0.8
}
uploadUrl = f"http://localhost:{3010 if test else 3000}/uploads.json?api_key={testKey if test else prodKey}&login={user}"
def postUrl(page=1):
    return f"http://localhost:{3010 if test else 3000}/posts.json?api_key={testKey if test else prodKey}&login={user}&page={page}"
if __name__ == '__main__':
    basePath = input("Base Path: ")
    batchTag = input("Batch Tag: ") or []
    main(basePath, batchTag)