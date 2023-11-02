import os
from langchain.utilities.bing_search import BingSearchAPIWrapper
from langchain.chat_models import AzureChatOpenAI
import os
from langchain.schema import (
    HumanMessage,
    SystemMessage
)
import json
import time
# 设置search

os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"

# 设置langsmith
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'

os.environ['LANGCHAIN_PROJECT'] = 'zhihe'

# 设置openai环境变量
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-05-15" 
os.environ["OPENAI_API_BASE"] = "https://zhiexagpt4.openai.azure.com/" 


# 初始化模型
chat = AzureChatOpenAI(
            deployment_name="zhiexagpt4",
            temperature=0)


# search = BingSearchAPIWrapper()
# print(search.run("退休后还可以重新签订劳动合同吗"))


system_template = r"""
你是强大的法律AI助手ChatGPT。\n
现在你的角色是精英律师。\n
你需要用律师的方式回答用户的问题。\n
你回答问题的格式是首先精准的给出用户答案，然后分析用户问题涉及的法律问题。
格式模板：
# 答案:
    .......
# 分析:
    .......
    .......
"""

def llm_serach_answer(question):
    search = BingSearchAPIWrapper()
    search_answer = search.run(question)
    messages = [
    SystemMessage(content=system_template),
    HumanMessage(content=f"""
        下面是问题相关的网页搜索内容：\n
        --------------------------\n
        {search_answer}\n
        --------------------------\n
        你需要从这些信息中删选出来和问题相关的信息协助解答用户问题！\n
        用户问题:\n
        --------------------------\n
        {question}\n
        --------------------------\n
        """)
    ]
    res = chat(messages).content
    return res
