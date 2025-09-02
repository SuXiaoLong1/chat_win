


# from openai import OpenAI
# from context import context

from deepseek_api.baseApi import baseApi
class careHeart(baseApi):
    def __init__(self,url=None,api_key=None,model=None):
        # 初始化API参数
        if url is None:
            url = "https://openrouter.ai/api/v1"
        if api_key is None:
            api_key = "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"
        if model is None:
            model="deepseek/deepseek-chat-v3.1"
        super().__init__(api_key, url,model)
        # 初始化API参数
        self.model=model
        self.name = "careHeart"
        self.version = "V3_0324_free"
        self.description = "深度寻心AI助手，基于深度寻心模型，提供多种功能的API接口。"



if __name__ == '__main__':

    a=careHeart()
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
        completion = a.answer(question)
        print(completion)

    # print(completion)

