#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import time
from os import times
from pprint import pprint
import re
import json
import requests
# from ..MusicBox.MusicPlayer.apis.netEaseApi import NetEaseWebApi

from MusicBox.MusicPlayer.apis.apiRequestsBase import *
from MusicBox.MusicPlayer.apis.netEaseApi import *

# print(NetEaseWebApi)
# t = t_obj.all_playlist(cat='全部歌单', types='all', offset=30, index=1)
# print(t)
# print(type(t))

time.sleep(1111)



f = open("49w+歌曲信息(6400名内地+港台歌手)", encoding="utf-8")
print(f)
print(type(f))
# for i in f.read():
#     print(i)
file = open("49w+歌曲信息(6400名内地+港台歌手)", encoding="utf-8")
line = file.readline()
while line:
    line = json.loads(line)
    print(type(line), line)
    print(line['song_mid'])
    play_url = "https://y.qq.com/n/yqq/song/%s.html" % line['song_mid']
    print(play_url)
    line = file.readline()

    time.sleep(1)
file.close()
# u_ = 'https://dataiqs.com/api/kwmusic/?msg=起风了&type=&n=0'
# # u_ = 'https://dataiqs.com/api/netease/music/?type=random'
# x = requests.post(u_)
# # 返回网页内容
# print(x.json())
#
# time.sleep(1111)
# - coding: utf-8 -*-
import requests
import json
import os

from Demos.mmapfile_demo import page_size

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


# 获取指定歌手的歌曲信息
def get_artist_songs(artist_id):
    """
    发送请求获取指定歌手的歌曲信息
    参数:
    artist_id (str): 歌手的 ID
    返回:
    list or None: 成功则返回歌曲列表，否则返回 None
    """
    url = 'https://music.163.com/api/v1/artist/songs'  # 歌手歌曲信息 API 的 URL
    params = {
        'id': artist_id,  # 歌手 ID
        'offset': 0,  # 偏移量
        'total': True,  # 是否获取全部歌曲信息
        'limit': 1000  # 获取歌曲数量
    }
    try:
        response = requests.get(url, headers=headers, params=params)  # 发送 GET 请求
        response.raise_for_status()  # 如果响应状态码不是 200，抛出异常
        result = json.loads(response.text)  # 将响应的文本内容转为 JSON 格式
        songs = result['songs']  # 获取歌曲列表
        return songs
    except requests.exceptions.RequestException as e:
        print('请求出错:', e)  # 打印请求错误信息
        return None


# 下载歌曲
def download_song(song_name, song_url, save_dir):
    """
    下载指定歌曲并保存到指定目录
    参数:
    song_name (str): 歌曲名称
    song_url (str): 歌曲的下载 URL
    save_dir (str): 保存歌曲的目录
    """
    if not os.path.exists(save_dir):  # 如果保存目录不存在，则创建目录
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, '{}.mp3'.format(song_name))  # 拼接保存路径和文件名
    if os.path.exists(save_path):  # 如果文件已存在，则跳过下载
        print('{} 已存在，跳过下载！'.format(song_name))
        return
    try:
        response = requests.get(song_url, headers=headers)  # 发送 GET 请求
        response.raise_for_status()  # 如果响应状态码不是 200，抛出异常
        with open(save_path, 'wb') as f:  # 以二进制写入模式打开文件
            f.write(response.content)
        print('{} 下载完成！'.format(song_name))  # 打印下载完成信息
    except requests.exceptions.RequestException as e:
        print('{} 下载失败！'.format(song_name))  # 打印下载失败信息


# 获取歌曲名称和播放链接
def get_song_info(song):
    """
    从歌曲数据中提取歌曲名称和播放链接
    参数:
    song (dict): 包含歌曲信息的字典
    返回:
    tuple: 歌曲名称和播放链接的元组
    """
    song_name = song['name']  # 歌曲名称
    song_id = song['id']  # 歌曲 ID
    url = 'https://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)  # 歌曲播放链接
    return song_name, url


# 主函数
if __name__ == '__main__':
    artist_id = '2116'  # 歌手 ID，这里以陈奕迅为例，歌手 ID 可以在网易云音乐上搜索歌手，进入歌手的主页，查看 URL 中的 ID 参数即为该歌手的 ID
    num_songs = 10  # 下载歌曲数量
    songs = get_artist_songs(artist_id)  # 获取歌手的歌曲信息
    print(songs)
    if songs:
        save_dir = '陈奕迅歌曲'  # 保存目录
        for i, song in enumerate(songs):
            if i >= num_songs:
                break
            # song_name, song_url = get_song_info(song)  # 获取歌曲名称和播放链接
            # print(song)
            print('++++++++++++++++++++++++++++++++++++')
            print()
            print()
            pprint(song)
            tmp_dict = {
                'song_name': song['name'],
                'song_id': song['id'],
                'singer_image': song['album']['blurPicUrl'],
                'url': 'https://music.163.com/song/media/outer/url?id={}.mp3'.format(song['id'])
            }
            print(tmp_dict)
    time.sleep(1111)
    #         # download_song(song_name, song_url, save_dir)  # 下载歌曲
    # else:
    #     print('获取歌曲信息失败！')  # 如果获取歌曲信息失败

    # https://www.kugou.com/yy/rank/home/1-8888.html?from=rank
    def get_encode_album_audio_id(url='https://www.kugou.com/yy/rank/home/2-8888.html?from=rank'):
        dic_headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'cookie': 'kg_mid=a1dd2b6ab4362156489644e5687fc1e4; kg_dfid=3exUvM3tv8Ms22pf5b2n00JB; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1692943898; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1692950108',
            'referer': 'https://www.kugou.com/',
        }
        response = requests.get(url, headers=dic_headers)
        html = response.text
        encode_album_audio_id = re.findall(r'data-eid="(.*?)"', html)
        print(len(encode_album_audio_id), encode_album_audio_id)


    # get_encode_album_audio_id()

    # 创建多页的url
    urls = ["http://www.kugou.com/yy/rank/home/{}-8888.html".format(number) for number in range(1, 24)]
    for item_url in urls:
        print(item_url)
        get_encode_album_audio_id(item_url)
        time.sleep(1)

