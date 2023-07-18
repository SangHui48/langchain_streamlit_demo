import os
import pickle
import openai
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from streamlit_chat import message

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# from PIL import Image
# robots = Image.open('./gpt.png')

# Sidebar contents
with st.sidebar:
    st.title('🤗💬 LLM Chat App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model
 
    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ by [Prompt Engineer](https://youtube.com/@engineerprompt)')

def main():

    styl = f"""
    <style>
        .stTextInput {{
        position: fixed;
        bottom: 3rem;
        }}
    </style>
    """
    st.markdown(styl, unsafe_allow_html=True)
    st.header("Chat with PDF 💬")
    load_dotenv()

    # upload a PDF file
    pdf = st.file_uploader("Upload your PDF", type="pdf")

    if pdf is not None:
        pdf_reader = PdfReader(pdf)

        # text = ""
        # for page in pdf_reader.pages:
        #     text += page.extract_text()
        
        # text_splitter = RecursiveCharacterTextSplitter(
        #     chunk_size=1000,
        #     chunk_overlap=200,
        #     length_function=len
        # )

        # chunks = text_splitter.split_text(text=text)
        
        # # Embeddings
        # store_name = pdf.name[:-4]
        # st.write(f'{store_name}')

        # if os.path.exists(f"{store_name}.pkl"):
        #     with open(f"{store_name}.pkl", "rb") as f:
        #         VectorStore = pickle.load(f)
        #     st.write("Embeddings Loaded from the Disk")
        # else:
        #     embeddings = OpenAIEmbeddings()
        #     VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
        #     with open(f"{store_name}.pkl", "wb") as f:
        #         pickle.dump(VectorStore, f)
            
        #     st.write('Embeddings Computation Completed')

        # Accept user questions/query
        chat = ChatOpenAI(temperature=0)
        if "messages" not in st.session_state:
            st.session_state.messages = [
                SystemMessage(content="You are a helpful assistant.")
            ]
        query = st.chat_input("Your message: ", key="user_input")
        if query:
            st.session_state.messages.append(HumanMessage(content=query))
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))
            # query += ' 한국어로 대답해줘.'
            # docs = VectorStore.similarity_search(query=query, k=3)

            # llm = OpenAI(model_name='gpt-3.5-turbo')
            # chain = load_qa_chain(llm=llm, chain_type='stuff')
            # with get_openai_callback() as cb:
            #     response = chain.run(input_documents=docs, question=query)
            #     print(cb)
            # st.write(response)

        messages = st.session_state.get('messages', [])
        for i, msg in enumerate(messages[1:]):
            if i % 2 == 0:
                with st.chat_message("user"):
                    st.write(msg.content, key=str(i) + '_user')
                    # message(msg.content, is_user=True, key=str(i) + '_user')
            else:
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    full_response += msg.content.delta.get("content", "")
                    message_placeholder.markdown(full_response + "▌")
                    # st.write(msg.content, key=str(i) + '_ai')
                # message(msg.content, is_user=False, key=str(i) + '_ai')


if __name__ == '__main__':
    main()