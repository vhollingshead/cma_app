import streamlit as st
from streamlit_chat import message
from pinecone_db import chatbot_
import re
# from wikiwrapper import wiki_wrapper

# Access the OpenAI API key
openai_api_key = st.secrets["api_key"]

def replace_unknown_response(input_string):
    replacement_message = ("Ako ay humihingi ng paumanhin. Hindi ko masagot ang tanong na iyon, "
                           "mangyaring sumangguni sa Center for Migrant Advocacy Direct Assistance "
                           "para sa tulong: https://www.facebook.com/centerformigrantadvocacyph/")
    
    if "Hindi ko alam" in input_string or "I don't know" in input_string:
        return replacement_message
    return input_string

def convert_string(input_str):
    print('this is the input str before:', input_str)
    acronyms = ["polo", "sena", "owwa", "mwo"]
    input_str = input_str.lower()
    # Check if any acronym is in the input string
    if any(acronym in input_str for acronym in acronyms):
        for acronym in acronyms:
            input_str = input_str.replace(acronym, acronym.upper())
            print('this is input str 1:', input_str)
    else:
        input_str = input_str.lower()
        print('this is input str 2:', input_str)
    return input_str

def chatbot_greeting(level1, level2=None):
    message = st.chat_message("assistant")
    if level2 == None:
        level2 = level1
    converted_string = convert_string(level2)
    print('this is the convereted string:', converted_string)
    message.write(f"Ano ang iyong katanungan tungkol sa {converted_string}?")

def user_response(main_topic, sub_topic):
    with st.chat_message("user"):
        user_question = st.text_input("Mayroon akong tanong na ito...", key="user_question")
        if user_question:
            query = user_question
            # response = retrieve_response(user_question) # basic response
            response = chatbot_(query, main_topic, sub_topic)
            no_hindi_ko_alam = replace_unknown_response(response)
            st.session_state.modified_answer = no_hindi_ko_alam
            st.session_state.step = 9

def feedback(feedback_to_state):
    message_td2 = st.chat_message("assistant")
    message_td2.write(st.session_state.modified_answer)
    message_td2.write(f"Nasagot ba ang iyong katanungan?") 
    thumbs_up, thumbs_down = st.columns(2)
    if thumbs_up.button("👍", key="thumbs_up2"):
        st.session_state.step = feedback_to_state
    elif thumbs_down.button("👎", key="thumbs_down2"):
        st.session_state.step = feedback_to_state

def chatbot_followup(mayroon_q_to_state_meron, mayroon_q_to_state_wala):
    message_tu = st.chat_message("assistant")
    message_tu.write("Salamat po sa inyong feedback!  Mayroon ka pa bang ibang tanong?")

    yes, no = st.columns(2)
    if yes.button("✅ Meron po", key="yes"):
        st.session_state.step = mayroon_q_to_state_meron
        st.rerun()
    elif no.button("❌ Wala na po", key="no"):
        st.session_state.step = mayroon_q_to_state_wala
        st.rerun()

def wala_q():
    message_tu5 = st.chat_message("assistant")
    message_tu5.write("Salamat sa pakikipag-ugnayan! Kung may iba ka pang tanong, narito lang ako.")

def chat_ensemble(level1, level2):
    print('DEVELOPER NOTE: Entering Ensemble')
    if st.session_state.step == 1:
        print('DEVELOPER NOTE: Chat Greeting')
        chatbot_greeting(level1, level2)
        st.session_state.step = 8
    if st.session_state.step == 8:
        print('DEVELOPER NOTE: User Response')
        user_response(main_topic = level1, sub_topic = level2)
    if st.session_state.step == 9:
        print('DEVELOPER NOTE: User Feedback')
        feedback(feedback_to_state=10)
    if st.session_state.step == 10:
        print('DEVELOPER NOTE: More Questions')
        chatbot_followup(mayroon_q_to_state_meron=8, mayroon_q_to_state_wala=12)
    if st.session_state.step == 12:
        print('DEVELOPER NOTE: End Ensemble')
        wala_q()

def wala_ensemble(level1, level2):
    print('DEVELOPER NOTE: Entering Ensemble')
    if st.session_state.step == 1:
        print('DEVELOPER NOTE: Chat Greeting')
        chatbot_greeting(level1)
        st.session_state.step = 8
    if st.session_state.step == 8:
        print('DEVELOPER NOTE: User Response')
        user_response(main_topic = level1, sub_topic = level2)
    if st.session_state.step == 9:
        print('DEVELOPER NOTE: User Feedback')
        feedback(feedback_to_state=10)
    if st.session_state.step == 10:
        print('DEVELOPER NOTE: More Questions')
        chatbot_followup(mayroon_q_to_state_meron=8, mayroon_q_to_state_wala=12)
    if st.session_state.step == 12:
        print('DEVELOPER NOTE: End Ensemble')
        wala_q()