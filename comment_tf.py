# -*- coding: utf-8 -*-

# コメントのJSONを入力すると、各コメントを文単位に分割・クリーニングし、コメントの重複数をそのtf値として出力
# 重複数が1のものは、1/log2(コメントの長さ)をtf値とする

import json
import argparse
import math
import re

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', dest='json', type=str, default='NONE', metavar='PATH',
                        help='chat JSON filename')
    parser.add_argument('--json2', dest='json2', type=str, default='NONE', metavar='PATH',
                        help='chat JSON filename')
    parser.add_argument('--N', dest='N', type=int, default=10, metavar='NUM',
                        help='N for Ngrams')
    return parser

def get_data(target_json, data_list):
    f = open(target_json, 'r')
    json_data = json.load(f)
    for comment_info in json_data:
        # コメント
        text = comment_info['snippet']['topLevelComment']['snippet']['textDisplay']
        # print('{}\n{}\nグッド数: {} 返信数: {}\n'.format(cnt, text, like_cnt, reply_cnt))
        text_split = re.split('[、。，．,\.\n]', text)
        for t in text_split:
            text_findall = re.findall('.*?[!\?！？]|.*$', t)
            for t in text_findall:
                if t not in ['', ' ', '　', '!', '！', '?', '？'] and '\n' not in t:
                    data_list.append(t)
        # data_list += text_split
    return data_list
        
def show(data_list):
    dict_comment = {}
    for text in data_list:
        if text not in dict_comment.keys():
            dict_comment[text] = 0
        dict_comment[text] += 1
    for k, v in sort_dict(dict_comment):
        print(k,v)
    
def sort_dict(dict_comment):
    return [(k, v) for k, v in sorted(dict_comment.items(), key=lambda x: -x[1])]
    
def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.json != 'NONE':
        target_json = args.json
        target_json2 = args.json2
    else:
        target_json = input("Enter chat JSON filename : ")
    data_list = []
    data_list = get_data(target_json, data_list)
    data_list = get_data(target_json2, data_list)
    show(data_list)
    
if __name__=='__main__':
    main()
