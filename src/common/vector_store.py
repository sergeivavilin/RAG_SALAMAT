from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from src.settings.config import PineconeSettings

settings = PineconeSettings()


class VectorStore:
    def __init__(self) -> None:
        self.config = settings

        self.pc = Pinecone(api_key=self.config.pinecone_api_key)
        self.index = self.pc.Index(
            name=self.config.index_name, host=self.config.index_host
        )

        self.embedding = OpenAIEmbeddings(
            model=self.config.embedding_model,
            dimensions=self.config.dimension,
            openai_api_key=self.config.openai_api_key,
        )

        self.vector_store = PineconeVectorStore(
            index=self.index, embedding=self.embedding, namespace=self.config.namespace
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size, chunk_overlap=self.config.chunk_overlap
        )

        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"namespace": self.config.namespace}
        )

    def search(self, query: str) -> str:
        """Поиск по векторной базе через retriever.
        Возвращает текстовые результаты."""
        results = self.retriever.invoke(query)
        # results может быть списком документов или строк
        if isinstance(results, list):
            # Если это список документов, склеим их содержимое
            return "\n".join(str(doc) for doc in results)
        return str(results)


vector_store = VectorStore()
