import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()

if not os.getenv("PINECONE_API_KEY"):
    raise ValueError("PINECONE_API_KEY not found in environment variables")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index(
    # name="n8n-salamat-names",
    # host="https://n8n-salamat-names-rkhbx77.svc.aped-4627-b74a.pinecone.io",
    name="salamat-names",
    host="https://salamat-names-rkhbx77.svc.aped-4627-b74a.pinecone.io",
)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1536)
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

retriever = vector_store.as_retriever(
    search_kwargs={"namespace": "price without costs"}
)


def search_vector_store(query: str) -> str:
    """Поиск по векторной базе через retriever. Возвращает текстовые результаты."""
    results = retriever.invoke(query)
    # results может быть списком документов или строк
    if isinstance(results, list):
        # Если это список документов, склеим их содержимое
        return "\n".join(str(doc) for doc in results)
    return str(results)
