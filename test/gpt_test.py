

from openai import OpenAI
import requests
import json
app_key = 'sk-83a84ea88cc34698b95357513cdffdf9'

url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
# client = OpenAI(
#     api_key=app_key,  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
# )
# completion = client.chat.completions.create(
#     model="qwen-turbo",
#     messages=[
#         {'role': 'system', 'content': 'You are a helpful assistant.'},
#         {'role': 'user', 'content': '你是谁？'}],
#     temperature=0.8,
#     top_p=0.8
# )
# print(completion.model_dump_json())



headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer ' + app_key}
data = {
    "model": "qwen-turbo",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "你是谁？"
        }
    ]
}

a = requests.post(url, headers=headers, data=json.dumps(data))
print(a.text)