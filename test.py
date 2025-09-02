## 测试ONNX模型
# from model.onnxmodel import net
# import numpy as np
# ONNX_MODEL_PATH = "F:/python/visualization/chat_win/model/model.onnx"  # 替换为你的ONNX模型路
# net1=net(ONNX_MODEL_PATH,4)
# def get_data():
#     # return torch.rand(64, 500)
#     return np.random.randn(1, 1,64,500).astype(np.float32)
# EEG_doctor = net1.predict(get_data())
# print(EEG_doctor)

#测试子网页
# from flask import Flask, render_template, request, session, send_file, make_response
# from Get_data import init_app as init_getdata
# from log_util import init_logger
# import os
# DATA_DIR = os.path.dirname(__file__)+"/" + "data"  # 数据存储目录
# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(24)
# init_getdata(app)  # 注册子网页，子网页路由生效
# logger = init_logger(file_name=os.path.join(DATA_DIR, "running.log"), stdout=True)
# def check_session(current_session):
#     """
#     检查session，如果不存在则创建新的session
#     :param current_session: 当前session
#     :return: 当前session
#     """
#     if current_session.get('session_id') is not None:
#         pass
#         logger.debug("existing session, session_id:\t{}".format(current_session.get('session_id')))
#     else:
#         current_session['session_id'] = uuid.uuid1()
#         logger.info("new session, session_id:\t{}".format(current_session.get('session_id')))
#     return current_session['session_id']
# # os.getenv("PORT", default=PORT)
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     """
#     主页
#     :return: 主页
#     """
#     check_session(session)
#     return render_template('index.html')
# app.run(host="0.0.0.0", port=5000, debug=False)


# import mdraModel    
# print(mdraModel.mdraModel())





from deepseek_api.baseApi import baseApi
class careHeart(baseApi):
    def __init__(self,url=None,api_key=None,model=None):
        # 初始化API参数
        if url is None:
            url = "https://openrouter.ai/api/v1"
        if api_key is None:
            api_key = "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"
        if model is None:
            model="deepseek/deepseek-chat-v3-0324:free"
        super().__init__(api_key, url,model)
        # 初始化API参数
        self.model=model
        self.name = "careHeart"
        self.version = "V3_0324_free"
        self.description = "深度寻心AI助手，基于深度寻心模型，提供多种功能的API接口。"



if __name__ == '__main__':
    url = "https://openrouter.ai/api/v1"
    api_key = "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"
    model = "deepseek/deepseek-r1:free"
    a=careHeart(url, api_key, model)
    # question = "我有点头疼，应该怎么办？"
    # completion = a.answer(question)
    # print(completion)
    # completion = a.answer("- 抑郁倾向概率：0.52\
    #           - 患者疑问：“我是不是心理出问题了？我最近真的很没精神，也懒得社交。”\
    #             请以面向患者的语气写一段安抚性、正向的文字。")
    while True:
        
        question = input("请输入问题：")
        if question == "exit":
            break
        # completion = a.answer(question)
        # print(completion)
        try:
            for chunk in a.answer_stream(question):
                print(chunk,end='')
        except Exception as e:
            print(f"Error occurred: {e}")
            print("服务器繁忙，请稍后再试。")
        print('')

    # print(completion)


# import os
# from read_data.read_eeg_file import get_data
# from model.onnxmodel import net
# path = os.path.dirname(os.path.abspath(__file__))
# ONNX_MODEL_PATH = os.path.join(path, "model/model.onnx")  # ONNX模型路径



# net1=net(ONNX_MODEL_PATH,4)
# EEG_doctor = net1.predict(get_data())
# print(EEG_doctor)


# result_data = "<p><strong>抑郁症检测分析报告</strong></p>" \
#         f"<p>1. EEG信号分析：患者存在轻度异常脑电活动，抑郁症可能性为 <strong>{0.25:.2f}</strong></p>\n" \
#         f"<p>2. 音频特征分析：语音语调平缓，情绪低落特征明显，可能性为 <strong>{0.66:.2f}</strong></p>\n" \
#         f"<p>3. 文本语义分析：存在负面情绪词汇，自述内容符合抑郁症状，可能性为 <strong>{0.25:.2f}</strong></p>\n"
# print(result_data)