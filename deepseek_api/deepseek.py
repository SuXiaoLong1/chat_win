from openai import OpenAI
from baseApi import baseApi
class deepseek(baseApi):
    def __init__(self, api_key=None, base_url=None):
        if api_key is None:
            api_key = "sk-cdf6a76d34864bc09f75483290011280"
        if base_url is None:
            base_url = "https://api.deepseek.com"
        super().__init__(api_key, base_url)
        self.model = "deepseek-chat"



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


if __name__ == "__main__":
    # Initialize the API client
    api_key = "sk-cdf6a76d34864bc09f75483290011280"
    base_url = "https://api.deepseek.com"
    client = deepseek(api_key, base_url)
    print("Welcome to the DeepSeek Chatbot!")
    a=client.chat("你好")
    print(a)

    # while True:
    #     message = input("You: ")
    #     if message == "/bye":
    #         break
    #     response = chat(message)
    #     print(f"AI: {response}")