# -*- coding: utf-8 -*-
import pandas as pd
from flask import Flask, jsonify, request

from backend.goods.data_get_jd_goods_info import func_get_goods_info_jd
from backend.goods.rank_goods_home_recommend import func_main_goods_home_recommend

pd.set_option('expand_frame_repr', False)  # 显示的时候不换行
pd.set_option('display.max_columns', None)  # 显示所有列


app = Flask(__name__)


@app.route('/goods/home/recommend', methods=['POST'])
def predict_generate_image():
    """
curl.exe -X POST 'http://127.0.0.1:8528/goods/home/recommend' -H 'Content-Type:application/json' -d '{"user_id":"oNfQV6XQaAornDjN6xg-9GOqnba8", "page_index": 1, "page_size": 10}'
    """
    try:
        input_parameter = request.get_json()
        print(input_parameter)
        parm = {
            'page_index': input_parameter['page_index'],
            'page_size': input_parameter['page_size']
        }
        res_return = func_main_goods_home_recommend(parm)
        res = {'res_data': res_return, 'num': len(res_return)}
    except Exception as ex:
        res = ex
    return res

if __name__ == '__main__':
    """
    综合服务
    """
    func_get_goods_info_jd()
    app.run(host='0.0.0.0', port=8528, debug=False)


