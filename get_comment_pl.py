# -*- coding: utf-8 -*-

# YouTubeのプレイリストのURLを入力すると、プレイリスト中の動画からコメントをAPIで取得してJSON形式で保存
# ファイル名のprefixを指定する
# 自分のAPI keyに書き換える

import requests
import json
import argparse
from pytube import YouTube
from pytube import Playlist
import time
import re

URL = 'https://www.googleapis.com/youtube/v3/'
API_KEY = 'Your API key'

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', dest='id', type=str, default='NONE', metavar='STR',
                        help='YouTube Video id')
    parser.add_argument('--n', dest='n', type=int, default=100, metavar='NUM',
                        help='Max Results (n <= 100)')
    return parser

def get_video_comment(video_id, n, pageToken):
    params = {
        'key': API_KEY,
        'part': 'snippet',
        'videoId': video_id,
        'order': 'time',
        'textFormat': 'plaintext',
        'maxResults': n,
    }
    if pageToken != 'HEAD':
        params['pageToken'] = pageToken
        
    response = requests.get(URL + 'commentThreads', params=params)
    resource = response.json()
    return resource

def main():
    parser = get_parser()
    args = parser.parse_args()
    pl_url = input("Enter YouTube Playlist URL : ")
    pl = Playlist(pl_url)
    pl.populate_video_urls()
    # or if you want to download in a specific directory
    print(pl.video_urls)
    first_num = int(input("Enter first NUM : "))

    download_path = '.'
    for i, target_url in enumerate(pl.video_urls):
        while True:
            try:
                yt = YouTube(target_url)
                print(yt.title)
                break
            except Exception:
                time.sleep(1)
                print('retry')
                continue
        video_id = target_url.split('=')[1]
        comment_data = []
        pageToken = 'HEAD'
        while pageToken != 'NONE':
            resource = get_video_comment(video_id, args.n, pageToken)
            comment_data += resource['items']
            if 'nextPageToken' in resource.keys():
                pageToken = resource['nextPageToken']
            else:
                pageToken = 'NONE'

        prefix = str(i+first_num).zfill(3) + '.'
        filename = prefix + re.sub(r'[\\/:*?"<>|]+','_',yt.title) + "_comment.json"        
        json_text = json.dumps(comment_data, ensure_ascii=False)
        with open(filename, mode='w', encoding="utf-8") as f:
            f.write(json_text)
        
if __name__=='__main__':
    main()
