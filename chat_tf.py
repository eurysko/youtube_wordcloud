# -*- coding: utf-8 -*-

# チャットのJSONを入力すると、各コメントの先頭からn文字(1<=n<=N)の重複数を見て、重複数/log2(n)をその重複文字列のtf値として出力

import json
import argparse
import math

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', dest='json', type=str, default='NONE', metavar='PATH',
                        help='chat JSON filename')
    parser.add_argument('--N', dest='N', type=int, default=10, metavar='NUM',
                        help='N for Ngrams')
    return parser

def get_data(target_json):
    f = open(target_json, 'r')
    json_data = json.load(f)
    data_list = []
    for samp in json_data:
        d = {}
        try:
            samp = samp['replayChatItemAction']['actions'][0]['addChatItemAction']['item']
            if 'liveChatPaidMessageRenderer' in samp:
                d['message'] = samp['liveChatPaidMessageRenderer']['message']['simpleText']
            else:
                d['message'] = samp['liveChatTextMessageRenderer']['message']['simpleText']
        except Exception:
            continue
        data_list.append(d)
    return data_list

def show(data_list, N):
    dict_substr = {}
    substr = ''
    for d in data_list:
        prev_c = ''
        cnt_c = 0
        for c in ('*'+d['message']+'*')[:1+N]:
            if c == ' ':
                continue
            if c != prev_c:
                cnt_c = 0
            elif cnt_c >= 4:
                continue
            substr += c
            if substr not in dict_substr.keys():
                dict_substr[substr] = 0
            dict_substr[substr] += math.log2(len(substr))
            prev_c = c
            cnt_c += 1
        substr = ''
    for k, v in get_top_substr(dict_substr):
        if dict_substr[k] == 0 or len(k) <= 2:
            continue
        if v < 4:
            break
        print(k,v)
        for c in k[:-1]:
            substr += c
            dict_substr[substr] = 0
        substr = ''
    
def get_top_substr(dict_substr):
    return [(k, v) for k, v in sorted(dict_substr.items(), key=lambda x: -x[1])]
    
def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.json != 'NONE':
        target_json = args.json
    else:
        target_json = input("Enter chat JSON filename : ")
    data_list = get_data(target_json)
    show(data_list, args.N)
    
if __name__=='__main__':
    main()
