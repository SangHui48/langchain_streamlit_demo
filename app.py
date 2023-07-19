import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

from githubqa.get_info_from_api import github_api_call

# Sidebar contents
with st.sidebar:
    st.set_page_config(page_title = "This is a Multipage WebApp")
    st.title('🤗💬 LLM Chat App')
    add_vertical_space(5)
    st.write('Made with  by [오미자차](https://github.com/SangHui48/KDT_AI_B3)')
    

def main():
    load_dotenv()
    st.header("Gitter:feather: ")

    # user input github repo url
    github_link = st.text_input("Github repository github_link을 입력해주세요")

    if github_link is not None:
        # 2. 모든 데이터 "File_name" : "File_content" 형식 받아오기 
        github_info_dict, structure_content = github_api_call(github_link)
        st.write(github_info_dict)
        st.write(structure_content)
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
                    st.write(msg.content, key=str(i) + '_ai')
                # message(msg.content, is_user=False, key=str(i) + '_ai')


if __name__ == '__main__':
    main()