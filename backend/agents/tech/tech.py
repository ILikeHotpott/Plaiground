from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import SystemMessage, HumanMessage
import os
import requests

# 设置存储路径
VECTORSTORE_PATH = "tech_blogger_history"

# 初始化 GPT 模型
llm = ChatOpenAI(model="gpt-4o-2024-11-20", temperature=0.9)


# 初始化或加载向量存储
def initialize_vectorstore():
    embeddings = OpenAIEmbeddings()
    if os.path.exists(VECTORSTORE_PATH) and os.path.exists(f"{VECTORSTORE_PATH}/index.faiss"):
        vectorstore = FAISS.load_local(VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True)
        print("成功加载现有向量存储。")
    else:
        print("未找到现有向量存储，正在创建新的存储...")
        initial_texts = ["This is the first post.", "AI technology is evolving.", "Welcome to the tech blogger!"]
        vectorstore = FAISS.from_texts(initial_texts, embeddings)
        vectorstore.save_local(VECTORSTORE_PATH)
        print("新的向量存储已创建并保存。")
    return vectorstore


# 初始化向量存储
vectorstore = initialize_vectorstore()

# RAG 检索模块
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 工具 1：获取科技新闻
NEWS_API_URL = "https://newsapi.org/v2/everything?q=technology"
API_KEY = "818ac817f76d466faced185ac8121b1d"


def fetch_tech_news():
    params = {
        "q": "technology OR AI",  # 搜索科技或 AI 相关的文章
        "sortBy": "publishedAt",  # 按发布时间排序
        "apiKey": API_KEY  # 使用你的 NewsAPI 密钥
    }
    response = requests.get(NEWS_API_URL, params=params)
    data = response.json()

    # 检查返回的数据
    if response.status_code == 200 and data["status"] == "ok":
        articles = data["articles"][:5]
        news = [{"title": a["title"], "link": a["url"]} for a in articles]
        return news
    else:
        print("无法获取新闻:", data.get("message", "未知错误"))
        return []


news_tool = Tool(
    name="FetchTechNews",
    func=lambda _: fetch_tech_news(),
    description="Fetch the latest technology news articles."
)


# 工具 2：生成动态
def generate_post(news):
    # 假设 'news' 是一个包含 'title' 和 'link' 的字典列表
    formatted_news = "\n".join([f"{i + 1}. {item['title']} - {item['link']}" for i, item in enumerate(news)])

    # 使用 LangChain 生成动态
    messages = [
        SystemMessage(content="你是一个科技博主，每天都会发表最新科技动态。"),
        HumanMessage(content=f"""
        基于以下新闻，生成一条社交媒体动态，请以自然的语言讲述

        ### 新闻内容:
        {formatted_news}

        你可以风趣幽默，可以深刻分析，可以结合段子，也可以骂人，也可以严厉批评，也可以又一些讽刺的语言，根据不同的新闻内容你要自行选择语言风格,
        你不要用太多反问语句，而是要自己思考，你要有自己的见解，结尾不要写美好祝愿或者解决方案
        可以选择旗帜鲜明的表达出自己的观点，也可以含糊其辞，总之你的任务就是尽可能吸引读者的注意力
        
        """)
    ]
    response = llm.invoke(messages)
    return response.content


post_tool = Tool(
    name="GeneratePost",
    func=lambda news: generate_post(news),
    description="Generate a post based on news."
)

# 初始化记忆模块
memory = ConversationBufferMemory(memory_key="chat_history")

# 初始化 Agent
tools = [news_tool, post_tool]
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", memory=memory, verbose=True)


# 模拟任务执行
def run_daily_task():
    # 1. 获取新闻
    news = fetch_tech_news()
    formatted_news = "\n".join([f"{i + 1}. {item['title']} - {item['link']}" for i, item in enumerate(news)])

    # 2. 从历史动态中检索相关内容
    history = retriever.invoke(formatted_news)

    # 3. 生成动态
    post = generate_post(news)
    print("今日动态：")
    print(post)

    # 4. 将生成内容存入向量数据库
    vectorstore.add_texts([post])
    vectorstore.save_local(VECTORSTORE_PATH)
    print("动态已存储。")


if __name__ == "__main__":
    run_daily_task()
