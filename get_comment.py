# -*- coding: utf-8 -*-

# YouTubeのURLを入力すると、動画からコメントをAPIで取得しJSON形式で保存
# 自分のAPI keyに書き換える

import requests
import json
import argparse
from pytube import YouTube

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
    if args.id != 'NONE':
        video_id = args.id
    else:
        target_url = input("Enter YouTube Video URL : ")
        video_id = target_url.split('=')[1]
        yt = YouTube(target_url)      
        print(yt.title)
        
    comment_data = []
    pageToken = 'HEAD'
    while pageToken != 'NONE':
        resource = get_video_comment(video_id, args.n, pageToken)
        comment_data += resource['items']
        if 'nextPageToken' in resource.keys():
            pageToken = resource['nextPageToken']
        else:
            pageToken = 'NONE'

    json_text = json.dumps(comment_data, ensure_ascii=False)
    filename = yt.title.replace('/', '') + "_comment.json"
    with open(filename, mode='w', encoding="utf-8") as f:
        f.write(json_text)
            
if __name__=='__main__':
    main()
