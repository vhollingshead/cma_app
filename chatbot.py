import streamlit as st
from openai import OpenAI
from langchain_community.chat_models import ChatOpenAI
from streamlit_chat import message
from pinecone_db import retrieve_response_with_sources

# Access the OpenAI API key
openai_api_key = st.secrets["api_key"]

def convert_to_first_person(level1_button, level2_button, qa_string):
    # Convert question-answer pairs to a first-person narrative
    client_0 = OpenAI(api_key=openai_api_key)
    prompt = (
        "You are a case manager helping overseas Filipino workers in Saudi Arabia understand the Philipinnes judicial process.\n\n"
        f"The overseas Filipino worker's question is about {level1_button}.\n\n" 
        "Below are questions to show what information they need.\n\n"
        f"{qa_string}\n\n"
        "Combine this information to form a first-person query on behalf of the user:"
    )

    response = client_0.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=250,
        n=1,
        stop=None,
        temperature=0.7)
    
    answer = response.choices[0].message.content
    return answer

def custom_chatbot(level1_button, level2_button, query):
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
    converted_query = convert_to_first_person(level1_button, level2_button, query)
    # print(converted_query)

    # Get response from chatbot based on initial input

    initial_response = retrieve_response_with_sources(converted_query)
    answer_content = initial_response.get("answer", "Hindi ko alam ang sagot sa tanong na ito. Direktang makipag-ugnayan sa Center for Migrant Advocacy para sa tulong.")
    sources_content = initial_response.get("sources")
    source_documents_content = initial_response.get("source_documents")
    with st.chat_message("user"):
            st.markdown(converted_query)

    with st.chat_message("assistant"):
        st.markdown(answer_content)

    st.session_state.messages.append({"role": "user", "content": converted_query})
    st.session_state.messages.append({"role": "assistant", "content": answer_content})

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
        
        with st.chat_message("assistant"):
            # response = st.write_stream(stream)
            st.markdown(answer_stream)
        st.session_state.messages.append({"role": "assistant", "content": answer_stream})


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
    converted_query = f"May tanong ako tungkol sa {level1_button}."
    first_response = "Ano ang gusto mong malaman?"
    
    with st.chat_message("user"):
            st.markdown(converted_query)

    with st.chat_message("assistant"):
        st.markdown(first_response)

    st.session_state.messages.append({"role": "user", "content": converted_query})
    st.session_state.messages.append({"role": "assistant", "content": first_response})

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("May tanong ka ba?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})