from ollama import chat



from openai import OpenAI
class careHeart():
    def __init__(self,url=None,api_key=None,model=None):
        # 初始化API参数
        self._model="deepseek-r1:14b"
        self._url="http://localhost:11434/v1"
        self._api_key="ollama"
        if url is not None:
            self._url=url
        if api_key is not None:
            self._api_key=api_key
        if model is not None:
            self._model=model
        self.name = "careHeart"
        self.version = "V3_0324_free"
        self.description = "深度寻心AI助手，基于深度寻心模型，提供多种功能的API接口。"
        self.system_message = {"role": "system",
                                "content": "你是“医心大模型”，由类脑智能团队开发，具备专业的心理健康与精神医学知识，擅长识别和帮助有抑郁倾向的用户。\
                                            \
                                            你即将接收用户输入的**抑郁倾向概率**（如“有抑郁倾向的概率为0.78”）。请根据以下规则提供科学、同理心强、温和友好的建议：\
                                            \
                                            1. **温柔地解释概率含义**：\
                                               - 概率不是确诊结果，仅为心理状态的一个提示；\
                                               - 抑郁是一种常见且可管理的心理问题，越早关注越好。\
                                            \
                                            2. **提供支持建议**：\
                                               - 鼓励用户及时与亲友沟通；\
                                               - 提醒用户可以考虑进行心理咨询或评估；\
                                               - 推荐健康的生活方式（作息规律、运动、减少压力）。\
                                            \
                                            3. **避免恐慌和标签化**：\
                                               - 不使用“你已经抑郁症了”之类的断定性说法；\
                                               - 使用“可能存在”“建议关注”“值得重视”等温和措辞。\
                                            \
                                            4. **语气风格要求**：\
                                               - 同理、安慰、积极引导；\
                                               - 始终避免冷冰冰、命令式或否定性的语气。\
                                            \
                                            5. **提醒专业渠道**：\
                                               - 如概率较高，请建议用户联系专业心理医生进行线下评估；\
                                               - 同时说明“本模型不替代医生，仅提供建议”。\
                                            \
                                            你将根据用户提供的概率值，输出适度响应，避免过度反应或淡化问题。\
                                            "}
        self._ceilent=OpenAI(base_url=self._url, api_key=self._api_key)
        self._ceilent.chat.completions.create(
            model=self._model,
            messages=[self.system_message]
        )
        self.message=[self.system_message]
    def answer(self, question):
        self.message.append({"role": "user", "content": question})
        # 处理问题并生成回答
        response = self._ceilent.chat.completions.create(
            model=self._model,
            messages=self.message,
            temperature=0,
            stream=True
        )
        # self.message[-1]=[{"role": "user", "content": question},{'role': 'assistant', 'content': response.choices[0].message.content}]
        return response


if __name__ == '__main__':

    a=careHeart()
    question = "我有点头疼，应该怎么办？"
    completion = a.answer(question)
    for chunk in completion:
        # Print the chunk of text
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end='', flush=True)

    print(completion)






    # messages = [
    #
    # ]
    #
    # while True:
    #   user_input = input('Chat with history: ')
    #   response = chat(
    #     'deepseek-r1:14b',
    #     messages=messages
    #     + [
    #       {'role': 'user', 'content': user_input},
    #     ],
    #   )
    #
    #   # Add the response to the messages to maintain the history
    #   messages += [
    #     {'role': 'user', 'content': user_input},
    #     {'role': 'assistant', 'content': response.message.content},
    #   ]
    #   print(response.message.content + '\n')