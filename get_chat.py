# -*- coding: utf-8 -*-

# YouTubeライブのアーカイブのURLを入力すると、チャットのリプレイからチャットをスクレイピングしてJSON形式で保存

from bs4 import BeautifulSoup
import json
import requests
from pytube import YouTube
import re

def get_chat(target_url):
    dict_str = ""
    next_url = ""
    comment_data = []
    session = requests.Session()
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

    # まず動画ページにrequestsを実行しhtmlソースを手に入れてlive_chat_replayの先頭のurlを入手
    html = requests.get(target_url)
    soup = BeautifulSoup(html.text, "html.parser")

    for iframe in soup.find_all("iframe"):
        if("live_chat_replay" in iframe["src"]):
            next_url= iframe["src"]

    while(1):
        try:
            html = session.get(next_url, headers=headers)
            soup = BeautifulSoup(html.text,"lxml")

            # 次に飛ぶurlのデータがある部分をfind_allで探してsplitで整形
            for scrp in soup.find_all("script"):
                if "window[\"ytInitialData\"]" in scrp.text:
                    dict_str = scrp.text.split(" = ")[1]

            # javascript表記なので更に整形. falseとtrueの表記を直す
            dict_str = dict_str.replace("false","False")
            dict_str = dict_str.replace("true","True")
            
            # 辞書形式と認識すると簡単にデータを取得できるが, 末尾に邪魔なのがあるので消しておく（「空白2つ + \n + ;」を消す）
            dict_str = dict_str.rstrip("  \n;")
            # 辞書形式に変換
            dics = eval(dict_str)
        
            # "https://www.youtube.com/live_chat_replay?continuation=" + continue_url が次のlive_chat_replayのurl
            continue_url = dics["continuationContents"]["liveChatContinuation"]["continuations"][0]["liveChatReplayContinuationData"]["continuation"]
            next_url = "https://www.youtube.com/live_chat_replay?continuation=" + continue_url

            # dics["continuationContents"]["liveChatContinuation"]["actions"]がコメントデータのリスト。先頭はノイズデータなので[1:]で保存 
            # for samp in dics["continuationContents"]["liveChatContinuation"]["actions"][1:]:
            for samp in dics["continuationContents"]["liveChatContinuation"]["actions"]:
                comment_data.append(samp)
            
        # next_urlが入手できなくなったら終わり
        except:
            break
    return comment_data
    
def main():
    target_url = input("Enter YouTube Video URL : ")
    yt = YouTube(target_url)      
    print(yt.title)
    
    comment_data = get_chat(target_url)

    json_text = json.dumps(comment_data, ensure_ascii=False)
    filename = re.sub(r'[\\/:*?"<>|]+','_',yt.title) + "_chat.json"
    with open(filename, mode='w', encoding="utf-8") as f:
        f.write(json_text)
    
if __name__=='__main__':
    main()
