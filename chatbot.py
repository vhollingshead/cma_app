import streamlit as st
from openai import OpenAI
from streamlit_chat import message
from pinecone_db import chat_with_self_query_retriever, retrieve_response
from csv_db import get_value_from_csv
import os

# Access the OpenAI API key
openai_api_key = st.secrets["api_key"]

import streamlit as st


def replace_unknown_response(input_string):
    replacement_message = ("Ako ay humihingi ng paumanhin. Hindi ko masagot ang tanong na iyon, "
                           "mangyaring sumangguni sa Center for Migrant Advocacy Direct Assistance "
                           "para sa tulong: https://www.facebook.com/centerformigrantadvocacyph/")
    
    if "Hindi ko alam." in input_string or "I don't know" in input_string:
        return replacement_message
    return input_string

def custom_chatbot_intro(level2_button, level3_buttons):
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)
    
    if st.session_state.step == 1:
        message = st.chat_message("assistant")
        message.write(f"Hello, kumusta po kayo? Naiintindihan kong may tanong ka sa {level2_button}. Ano ang gusto mong matutunan?")
        st.session_state.step = 8

    if st.session_state.step == 8:
        sub_topic = st.session_state.path[1]
        options = level3_buttons[level2_button]
        options.insert(0, "Pumili mula sa ibaba:")

        with st.chat_message("user"):
            selected_option = st.selectbox("Mayroon akong tanong na ito:", options, key="question_select")

        if selected_option and selected_option != "Pumili mula sa ibaba:":
            st.session_state.selected_option = selected_option
            st.session_state.step = 9
            print("DEVELOPER NOTE: Successful session state step 8")

    if st.session_state.step == 9:
        print("DEVELOPER NOTE: Successful session state step 9")
        if st.session_state.selected_option:
            print("DEVELOPER NOTE: Successful session state step 9")

            message0 = st.chat_message("assistant")

            main_topic = st.session_state.path[0]
            sub_topic = st.session_state.path[1]
            selected_option = st.session_state.selected_option

            csv_answer = get_value_from_csv(main_topic, sub_topic, selected_option)

            message0.write(csv_answer)  # Replace with actual answer logic
            message0.write(f"Kapaki-pakinabang ba ang sagot na ito?")  # Replace with actual answer logic

        thumbs_up, thumbs_down = st.columns(2)
        if thumbs_up.button("👍", key="thumbs_up"):
            st.session_state.step = 10
        elif thumbs_down.button("👎", key="thumbs_down"):
            st.session_state.step = 11


    if st.session_state.step == 10:
        print("DEVELOPER NOTE: Successful session state step 10")
        message_tu = st.chat_message("assistant")
        message_tu.write("Salamat sa pag-confirm! Mayroon ka pa bang ibang tanong?")
            
        yes, no = st.columns(2)
        if yes.button("✅ Oo", key="yes"):
            st.session_state.step = 8
            st.experimental_rerun()
        elif no.button("❌ Hindi", key="no"):
            st.session_state.step = 12
            st.experimental_rerun()

    if st.session_state.step == 11:
        print("DEVELOPER NOTE: Successful session state step 11")
        message_td = st.chat_message("assistant")
        print("DEVELOPER NOTE: Successful session state step 11")
        print("the session state is:", st.session_state.step)
        
        message_td.write("Pasensya na, pwede bang pakilinaw ang tanong mo?")
        user_question = st.text_input("Ang tanong ko ay...", key="user_question")

        if user_question:
            print("DEVELOPER NOTE: Successful session state step 12")
            print("the session state step is:", st.session_state.step)
            main_topic = st.session_state.path[0]
            sub_topic = st.session_state.path[1]

            message_td2 = st.chat_message("assistant")
            # metadata = {
            #     "Main_Topic": main_topic,
            #     "Sub_Topic": sub_topic}
            # response, chat_history = chat_with_self_query_retriever(user_question, metadata, chat_history=None)
            response = retrieve_response(user_question)
            no_hindi_ko_alam = replace_unknown_response(response)
            message_td2.write(no_hindi_ko_alam)
            message_td2.write(f"Kapaki-pakinabang ba ang sagot na ito?")  # Replace with actual answer logic

            message_td3 = st.chat_message("assistant")

            thumbs_up, thumbs_down = st.columns(2)
            if thumbs_up.button("👍", key="thumbs_up2"):
                message_td3.write("Salamat sa iyong feedback.")
            elif thumbs_down.button("👎", key="thumbs_down2"):
                message_td3.write("Salamat sa iyong feedback.")


    if st.session_state.step == 12:
        message_tu5 = st.chat_message("assistant")
        message_tu5.write("Salamat sa pakikipag-ugnayan! Kung may iba ka pang tanong, narito lang ako.")

def wala_custom_chatbot_intro(level1_button):
    message = st.chat_message("assistant")
    message.write(f"Hello, kumusta po kayo? Naiintindihan kong may tanong ka sa {level1_button}. Ano ang gusto mong matutunan?")
    user_question = st.text_input("Ang tanong ko ay...", key="user_question")

    if user_question:
        print("DEVELOPER NOTE: Successful session state step 12")
        print("the session state step is:", st.session_state.step)
        message_td2 = st.chat_message("assistant")
        response = retrieve_response(user_question)
        no_hindi_ko_alam = replace_unknown_response(response)
        message_td2.write(no_hindi_ko_alam)


def wala_custom_chatbot(level1_button):
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Convert the question-answer pairs with a first-person query in natural language
    if "initial_response" not in st.session_state:
        query = f"May tanong ako tungkol sa {level1_button}."
        first_response = "Ano ang gusto mong malaman?"

        # Display the initial response
        with st.chat_message("user"):
            st.markdown(query)
        with st.chat_message("assistant"):
            st.markdown(first_response)

        # Store the initial response in session state
        st.session_state.messages.append({"role": "user", "content": query})
        st.session_state.messages.append({"role": "assistant", "content": first_response})
        st.session_state.initial_response = first_response
        st.session_state.query = query
    else:
        first_response = st.session_state.initial_response
        query = st.session_state.query

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("May tanong ka ba?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = retrieve_response_with_sources(prompt)
        answer_stream = stream.get("answer", "Hindi ko alam ang sagot sa tanong na ito. Direktang makipag-ugnayan sa Center for Migrant Advocacy para sa tulong.")
        sources_stream = stream.get("sources")
        source_documents_stream = stream.get("source_documents")

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            st.markdown(answer_stream)
        st.session_state.messages.append({"role": "assistant", "content": answer_stream})
