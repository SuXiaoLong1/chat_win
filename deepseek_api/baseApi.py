from openai import OpenAI
from .context import context
class baseApi():
    def answer_stream(self, question):
        """流式输出回答内容，每次 yield 一个内容片段"""
        self.message.append({"role": "user", "content": question})
        response = self._cilent.chat.completions.create(
            model=self._model,
            messages=self.message,
            stream=True
        )
        for chunk in response:
            delta = getattr(chunk.choices[0].delta, "content", None)
            if delta:
                yield delta
    def __init__(self, api_key=None, base_url=None,model=None):
        # self.client = OpenAI(api_key=api_key, base_url=base_url)
        # 初始化API参数
        self.model = ""

        # 初始化API参数
        self._url = base_url
        self._api_key = api_key
        self._model = model
        self.name = "base_API"
        self.version = "25.0.1"
        self.description = "api"
        self.__system_message = {"role": "system",
                                 "content": context}
        self._cilent = OpenAI(base_url=self._url, api_key=self._api_key)
        self._cilent.chat.completions.create(
            model=self._model,
            messages=[self.__system_message]
        )
        self.message = [self.__system_message]

    def answer(self, question):
        self.message.append({"role": "user", "content": question})
        # 处理问题并生成回答
        response = self._cilent.chat.completions.create(
            model=self._model,
            messages=self.message,
        )
        # self.message[-1]=[{"role": "user", "content": question},{'role': 'assistant', 'content': response.choices[0].message.content}]
        return response.choices[0].message.content

def chat(message):
    client = OpenAI(api_key="sk-cdf6a76d34864bc09f75483290011280", base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": message},
        ],
        stream=False
    )
    return response.choices[0].message.content


class ds(baseApi):
    def __init__(self, api_key, base_url):
        super().__init__(api_key, base_url)
        self.model = "deepseek-chat"

    def chat(self, message):
        response = self._cilent.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": message},
            ],
            stream=False
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    # Initialize the API client
    api_key = "sk-cdf6a76d34864bc09f75483290011280"
    base_url = "https://api.deepseek.com"
    client = baseApi(api_key, base_url)

    while True:
        message = input("You: ")
        if message == "/bye":
            break
        response = chat(message)
        print(f"AI: {response}")