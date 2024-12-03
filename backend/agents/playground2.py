import os
import bs4
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict

# 加载和处理文档
# 我们使用一个示例网站 URL 加载数据
url = "https://lilianweng.github.io/posts/2023-06-23-agent/"
loader = WebBaseLoader(
    web_paths=(url,),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(class_=("post-content", "post-title", "post-header"))
    ),
)
documents = loader.load()

# 文档切分为小块
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splitted_docs = text_splitter.split_documents(documents)

print(f"文档已被切分为 {len(splitted_docs)} 小段。")

# 嵌入和索引
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = FAISS.from_documents(splitted_docs, embeddings)

print("文档已被索引，向量数据库已建立。")


# 定义应用状态结构
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# 定义应用步骤
def retrieve(state: State):
    """检索与问题相关的文档片段。"""
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    """生成基于检索上下文的回答。"""
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    prompt = f"""
    你是一位智能助理，根据以下内容回答问题。
    如果你不知道答案，请直接说明“我不知道”。
    问题: {state["question"]}
    上下文: {docs_content}
    答案:"""
    llm = ChatOpenAI(model="gpt-4o-mini")
    response = llm.invoke(prompt)
    return {"answer": response.content}


# 构建和编译状态图
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

# 测试 RAG 应用
question = "What is Task Decomposition?"
response = graph.invoke({"question": question})

# 打印结果
print("问题:", question)
print("回答:", response["answer"])
