from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from get_info_from_api import github_api_call
from data_processing import dictionary_to_docs
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from vector_db import (
    db_from_pinecone, db_from_deeplake, mmr_retriever_setting
)

load_dotenv()

MODEL_NAME = "gpt-3.5-turbo-16k"

def main():
    # 1. 입력받기
    github_link = input("GitHub 링크를 입력해주세요 : ")

    # 2. 모든 데이터 "File_name" : "File_content" 형식 받아오기 
    github_info_dict, structure_content = github_api_call(github_link)
    
    # 3. "File_content 형식 데이터" 청킹 갯수 단위로 자른후에 리스트로 변환하기
    # 반환값 [Doc1, Doc2 ...] 
    docs = dictionary_to_docs(
        github_info_dict, structure_content,
        chunking_size=1000, overlap_size=0, 
        model_name=MODEL_NAME
    )

    # 4. chunking 된 데이터 vector db 로 임베딩 하기 
    # 임베딩 모델 및 vector db 반환 
    embedding_model = OpenAIEmbeddings(model='text-embedding-ada-002')
    
    # vector_db = db_from_deeplake(docs, embedding_model)
    vector_db = db_from_pinecone(docs, embedding_model)
    
    # 5. QA 를 위한 retriever 및 qa 세팅 하기 
    retriever =  mmr_retriever_setting(
        vectorstore=vector_db, 
        fetch_num=10, k_num=100
    )
    
    # 5. 원하는 질문 입력 하기 
    open_ai_model =  ChatOpenAI(model_name=MODEL_NAME)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=open_ai_model,
        memory=memory,
        retriever=retriever,
        get_chat_history=lambda h : h,
    )
    
    # 6. QA 시작
    questions = []
    answers = []
    while True:
        question = input("질문을 입력해주세요 : ")
        questions.append(question)
        
        result = qa_chain({"question": question})
        answers.append(result["answer"])
        
        print(f"**Answer**: {result['answer']} \n")
        
if __name__ == "__main__":
    main()