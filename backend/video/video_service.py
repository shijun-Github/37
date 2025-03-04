# -*- coding: utf-8 -*-
import json
import math
import os
import time
import sys
from datetime import datetime, timedelta
from pprint import pprint
from threading import Thread, Lock

from sklearn.utils import shuffle
from waitress import serve
import pandas as pd
import requests
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler


# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录（假设 aa_recommend_complete_project 是根目录下的一个包）
project_root = os.path.dirname(current_dir)
# 将项目根目录添加到 sys.path 中
sys.path.append(project_root)

# sys.path.append('..')  # 假设'..'是drama和utils的父目录
# from rank.drama_recommend_home import *
from video.recall import base_rec, keyword_search, search_func

pd.set_option('expand_frame_repr', False)  # 显示的时候不换行
pd.set_option('display.max_columns', None)  # 显示所有列

app = Flask(__name__)

# 定义全局变量, 定期更新， 例如将数据库中的内容定期更新到这个变量中就可以了
# 服务每次请求可以直接读取该变量，不需要去数据库中拉，极大提高速度
drama_info = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/drama_info.csv')
video_info = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/video_info.csv')
drama_info['drama_id'] = drama_info['drama_id'].astype(str)
video_info['drama_id'] = video_info['drama_id'].astype(str)
video_info['video_id'] = video_info['video_id'].astype(str)


def persist_data_in_service():
    global drama_info, video_info # 声明我们要使用全局变量
    drama_info = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/drama_info.csv')
    video_info = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/video_info.csv')
    drama_info['drama_id'] = drama_info['drama_id'].astype(str)
    video_info['drama_id'] = video_info['drama_id'].astype(str)
    video_info['video_id'] = video_info['video_id'].astype(str)
    print(drama_info)
    print(video_info)
    print('persist_data_in_service', time.time(), 'drama_info.shape:', drama_info.shape, 'video_info.shape:', video_info.shape)


def start_scheduler():
    """
    定时刷新数据
    redis_es_filter_realtime()
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(persist_data_in_service, 'interval', seconds=1*60)
    # scheduler.add_job(loadFaisIndex, 'interval', seconds=60 * 60)
    scheduler.start()


@app.route("/video/recommend", methods=["POST", "GET"])
def inter_drama_home_recommend():
    """
    打开软件，主页推荐页的
    """
    # global video_info  # 声明我们要使用全局变量
    t_s = time.time()
    if request.method == 'GET': parameters = request.args.to_dict()
    else: parameters = json.loads(request.get_data().decode("utf-8"))
    print("request data +++++++++", time.time(), parameters)
    video_page = base_rec.func_random_get_video(parameters, video_info)
    res_list_dict = video_page.to_dict(orient='records')
    res = {'res':
               {'data': res_list_dict}
           }
    print(time.time() - t_s)
    return res


@app.route("/video/drama/square", methods=["POST", "GET"])
def inter_drama_home_all():
    """
    剧目录页
    """
    # global drama_info  # 声明我们要使用全局变量
    t_s = time.time()
    parameters = json.loads(request.get_data().decode("utf-8"))
    print("request data +++++++++", time.time(), parameters)
    drama_page = base_rec.func_random_get_drama(parameters, drama_info)
    res_list_dict = drama_page.to_dict(orient='records')
    res = {'res':
               {'data': res_list_dict}
           }
    res = json.dumps(res, ensure_ascii=False)
    print('inter_drama_home_all()  /video/drama/square ', time.time() - t_s)
    return res

@app.route("/video/search/func_get_video_series_info_by_item_id", methods=["POST", "GET"])
def inter_func_get_video_series_info_by_item_id():
    """
    给关键词，返回一批剧
    """
    # global drama_info  # 声明我们要使用全局变量
    t_s = time.time()
    if request.method == 'GET': parameters = request.args.to_dict()
    else: parameters = json.loads(request.get_data().decode("utf-8"))
    print("request data +++++++++", time.time(), parameters)
    drama_page = search_func.func_get_video_series_info_by_item_id(parameters, video_info)
    res_list_dict = drama_page.to_dict(orient='records')
    res = {'res':
               {'data': res_list_dict}
           }
    res = json.dumps(res, ensure_ascii=False)
    print('inter_drama_home_all()  /video/drama/square ', time.time() - t_s)
    return res


@app.route("/video/search/func_search_drama_by_keyword", methods=["POST", "GET"])
def inter_func_search_drama_by_keyword():
    """
    给关键词，返回一批剧
    """
    # global drama_info  # 声明我们要使用全局变量
    t_s = time.time()
    if request.method == 'GET': parameters = request.args.to_dict()
    else: parameters = json.loads(request.get_data().decode("utf-8"))
    print("request data +++++++++", time.time(), parameters)
    drama_page = search_func.func_search_drama_by_keyword(parameters, drama_info)
    res_list_dict = drama_page.to_dict(orient='records')
    res = {'res':
               {'data': res_list_dict}
           }
    print(time.time() - t_s)
    return res

@app.route("/video/search", methods=["POST", "GET"])
def inter_drama_search():
    """
    给关键词，返回一批剧
    """
    global drama_info  # 声明我们要使用全局变量
    t_s = time.time()
    if request.method == 'GET': parameters = request.args.to_dict()
    else: parameters = json.loads(request.get_data().decode("utf-8"))
    print("request data +++++++++", time.time(), parameters)
    drama_page = keyword_search.func_key_word_search_drama(parameters, drama_info)
    res_list_dict = drama_page.to_dict(orient='records')
    res = {'res':
               {'data': res_list_dict}
           }
    print(time.time() - t_s)
    return res
    # pageNum = 1
    # pageSize = 10
    # keyword = "哈哈哈"
    # if "pageNum" in req:
    #     pageNum = req["pageNum"]
    # if "pageSize" in req:
    #     pageSize = req["pageSize"]
    # if "keyword" in req:
    #     keyword = req["keyword"]
    # t_s = time.time()
    # topic_id_set = get_invalid_id("hobby_rec_text_recall_topic_invalid_")
    # keyword_id_set = get_invalid_id("hobby_rec_text_recall_keyword_invalid_")
    # topic_data = func_faiss_drama_keyword_search(keyword, topic_faiss_index, 1, topic_id_set)
    # keyword_data = func_faiss_drama_keyword_search(keyword, keyword_faiss_index, 2, keyword_id_set)
    # re_data = topic_data + keyword_data
    # re_data = sorted(re_data, key=lambda x: x["score"])
    # start_index = (pageNum - 1) * pageSize
    # end_index = start_index + pageSize
    # page_data = re_data[start_index:end_index]
    # print('cost time: ', time.time() - t_s)
    # res = {
    #     "return_code": 0,
    #     "return_message": "success",
    #     "data": page_data
    # }
    # return res


if __name__ == '__main__':
    """
    服务
    gunicorn -w 4 -b 0.0.0.0:8528 start_service.py:app
    nohup python start_service.py

    该程序 已启动本地服务 ps -ef|grep start_service.py
    """
    print("扛起大刀。。。")
    start_scheduler()   # 定期刷新数据
    # print(os.path.dirname(os.path.abspath(__file__)))

    app.run(host='0.0.0.0', port=8588, debug=False)
    # serve(app, host='0.0.0.0', port=8588, threads=3)
    # app.run(host="0.0.0.0", port=8588, ssl_context="adhoc")