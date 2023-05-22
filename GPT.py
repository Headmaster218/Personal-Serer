
import openai
import os

# 将API密钥导入OpenAI SDK中
openai.api_key = "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"

# 定义请求函数
def ask(question, chat_log=None):
    response = openai.Completion.create(
        engine="davinci",
        prompt=chat_log + question,
        temperature=0.2,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    answer = response.choices[0].text
    return answer

# 开始会话
chat_log = ""
print("开始你的聊天：")

while True:
    # 获取用户输入问题
    user_input = input("> ")
    
    # 终止程序
    if user_input.lower() in ("exit", "quit"):
        break
    
    # 向API发送请求，并打印响应结果
    answer = ask(user_input, chat_log)
    chat_log += user_input + "\n" + answer + "\n"
    print(answer.strip())
