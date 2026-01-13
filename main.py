import base64
import time
from openai import OpenAI

def typewriter_effect(text, delay=0.03):
    """逐字输出文本"""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

client = OpenAI(
    api_key="sk-a3491504c3ca43929970107835719f47",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 读取本地图片
image_path = "./image.jpg"  # 修改为你的图片路径
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

print("正在分析图片...")

try:
    # 尝试流式输出
    completion = client.chat.completions.create(
        model="qwen-vl-plus",
        messages=[{"role": "user", "content": [
            {"type": "image_url", 
             "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
            {"type": "text", "text": "请为我导盲，20个字以内"}
        ]}],
        stream=True
    )
    
    print("分析结果：")
    for chunk in completion:
        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()
    
except Exception as e:
    print(f"流式模式不支持，使用标准模式...")
    
    # 标准模式
    completion = client.chat.completions.create(
        model="qwen-vl-plus",
        messages=[{"role": "user", "content": [
            {"type": "image_url", 
             "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
            {"type": "text", "text": "请为我导盲，20个字以内"}
        ]}],
        stream=False
    )
    
    full_response = completion.choices[0].message.content
    print("分析结果：")
    typewriter_effect(full_response)