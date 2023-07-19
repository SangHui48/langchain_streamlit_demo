import os
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone, DeepLake
from dotenv import load_dotenv

load_dotenv()

# pinecone db 임베딩 후 리턴
def db_from_pinecone(docs, embeddings):
    
    # initialize pinecone
    pinecone.init(
        api_key= os.getenv("PINECONE_API_KEY"),
        environment= os.getenv("PINECONE_ENV")  
    )
    index_name = os.getenv("PINECONE_INDEX_NAME") 
    
    # pinecone vector 삭제
    index = pinecone.Index(index_name)
    index.delete(deleteAll='true')
    vectorstore = Pinecone.from_documents(docs, embeddings, index_name=index_name)

    return vectorstore

def db_from_deeplake(docs, embeddings):
    # get it from https://app.activeloop.ai/
    user_name = os.getenv("DEEPLAKE_USERNAME")
    file_name = os.getenv("ACTIVELOOP_FILE_NAME")
    db = DeepLake.from_documents(
        docs, embeddings, dataset_path=f'hub://{user_name}/{file_name}'
    )

    db = DeepLake(
            dataset_path=f"hub://{user_name}/{file_name}",
            read_only=True,
            embedding_function=embeddings
    )
    return db

def mmr_retriever_setting(vectorstore, fetch_num, k_num):
    retriever = vectorstore.as_retriever(search_type="mmr")
    retriever.search_kwargs["distance_metric"] = "cos"
    retriever.search_kwargs["fetch_k"] = fetch_num
    retriever.search_kwargs["maximal_marginal_relevance"] = True
    retriever.search_kwargs["k"] = k_num
    
    return retriever
