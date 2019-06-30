# -*- coding: utf-8 -*-

# 各動画のチャットのtf値のファイルを含むディレクトリを入力として、idf値を出力する

import os
import argparse
import math

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', dest='dir', type=str, default='NONE', metavar='PATH',
                        help='chat dir path')
    return parser

def show(dir_path, file_list):
    dict_idf = {}
    for filename in file_list:
        with open(dir_path+'/'+filename) as f:
            lines = f.readlines()
        for line in lines:
            substr = line.split()[0]
            if substr not in dict_idf.keys():
                dict_idf[substr] = 0
            dict_idf[substr] += 1
    for k, v in get_top_substr(dict_idf):
        idf = math.log2(len(file_list)/v)
        print(k,idf)
    
def get_top_substr(dict_substr):
    return [(k, v) for k, v in sorted(dict_substr.items(), key=lambda x: x[1])]
    
def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.dir != 'NONE':
        dir_path = args.dir
    else:
        dir_path = input("Enter dir path : ")
    file_list = os.listdir(dir_path)
    show(dir_path, file_list)
    
if __name__=='__main__':
    main()
