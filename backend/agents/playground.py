from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# 加载本地数据
file_path = "data.txt"
with open(file_path, "w", encoding="utf-8") as f:
    f.write("""
yitong Liu的邮箱是liuyitong1210@163.com
他的年龄是25岁
他的职业是学生
他的爱好是看书
他的座右铭是“读万卷书，行万里路”
	""")

loader = TextLoader(file_path, encoding="utf-8")
documents = loader.load()

# 文本分块
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
docs = text_splitter.split_documents(documents)

# 嵌入模型和向量数据库
embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(docs, embeddings)

# 构建检索问答链
retriever = vector_store.as_retriever(search_kwargs={"k": 2})
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o"),
    retriever=retriever,
    return_source_documents=True,
)

# 使用 invoke 方法进行问答
query = "给我讲讲yitong liu这个人，用十分诗意化的语言"
result = qa_chain.invoke({"query": query})  # 使用 invoke

# 打印结果
print("问题:", query)
print("回答:", result["result"])
print("\n相关文档片段:")
for doc in result["source_documents"]:
    print(doc.page_content)
