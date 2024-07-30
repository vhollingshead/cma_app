
print("DEVELOPER NOTE: Page Accessed")
import os
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone # https://docs.pinecone.io/integrations/langchain#4-initialize-a-langchain-vector-store
from langchain_pinecone import PineconeVectorStore
# from openai import OpenAI
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_openai import ChatOpenAI
# from langchain.chains import RetrievalQA 
# from langchain.chains import RetrievalQAWithSourcesChain  
import streamlit as st

import pandas as pd
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_loaders import WebBaseLoader

from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains import ConversationalRetrievalChain

# from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage

print("DEVELOPER NOTE: Imports done")

# Set API keys
openai_api_key = st.secrets["api_key"]
pinecone_api_key = st.secrets["pinecone_api_key"]
os.environ['OPENAI_API_KEY'] = openai_api_key
os.environ['PINECONE_API_KEY'] = pinecone_api_key

print("DEVELOPER NOTE: API Keys Done")

# Embeddings model
st_model_name = "multi-qa-mpnet-base-cos-v1"
embeddings_model = HuggingFaceEmbeddings(model_name=st_model_name)

print("DEVELOPER NOTE: Embeddings Model Done")

print("DEVELOPER NOTE: API Keys Done")

# Pinecone Client
pc = Pinecone(
        api_key=pinecone_api_key)

index_name = "cme-app"
index = pc.Index(index_name)
print("Index Stats 1:")
index.describe_index_stats()

# Pinecone VectorStore
vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings_model)

print("DEVELOPER NOTE: Pinecone Initialized")

# Chat model 
# openai_llm = OpenAI(api_key= openai_api_key)
openai_llm = ChatOpenAI(model="gpt-3.5-turbo")

print("DEVELOPER NOTE: Chat model initialized")

# # Upsert Question-Answer .CSV to Pinecone DB
# basic_qa_csv_file_path = "repository/translated_responses.csv"
# df = pd.read_csv(basic_qa_csv_file_path)

# print("DEVELOPER NOTE: pandas df read")

# # Step 4: Process and insert data
# vectors = []
# for idx, row in df.iterrows():
#     inquiry = row['Sub_Topic_Question']
#     response = row['Established_Response_Tagalog']
#     metadata = {
#         'main_topic': row['Main_Topic'],
#         'sub_topic': row['Sub_Topic'] # add more metadata as necessary
#     }
    
#     # Embed the question and answer
#     inquiry_embedding = embeddings_model.embed_documents([inquiry])[0]
#     response_embedding = embeddings_model.embed_documents([response])[0]

#     # Use a unique ID for each entry
#     entry_id = f"vec{idx}"

#     # Append to vectors list
#     vectors.append({
#         'id': entry_id,
#         'values': inquiry_embedding,
#         'metadata': {
#             'inquiry': inquiry,
#             'response': response,
#             **metadata
#         }
#     })

# print("DEVELOPER NOTE: Vectors Appended")
# # Insert into Pinecone
# index.upsert(
#     vectors=vectors,
#     namespace="cma-app_csv"
# )

# print("DEVELOPER NOTE: CSV Uploaded")

# ## Upsert Informational PDFs to Pinecone DB
# chunk_size=1000
# chunk_overlap=300
# csv_file = 'repository/PDF_Links.csv'
# df = pd.read_csv(csv_file)

# # Step 4: Process and insert data
# vectors = []
# for idx, row in df.iterrows():
#     pdf_link = row['PDF_Link']
#     print('this is the pdf link:',pdf_link)
#     metadata = {
#         'main_topic': row['Main_Topic'],
#         'sub_topic': row['Sub_Topic'],
#         'sub_topic_question': row['Sub_Topic_Question'],
#         'pdf_link': pdf_link
#     }
    
#     # Load and extract text from the PDF using PyPDFLoader
#     loader = PyPDFLoader(pdf_link)
#     documents = loader.load()
    
#     # Split the documents into chunks
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#     chunks = text_splitter.split_documents(documents)
    
#     for chunk_idx, chunk in enumerate(chunks):
#         chunk_text = chunk.page_content
        
#         # Embed the chunk content
#         chunk_embedding = embeddings_model.embed_documents([chunk_text])[0]

#         # Use a unique ID for each chunk
#         entry_id = f"pdf-{idx}-chunk-{chunk_idx}"

#         # Append to vectors list
#         vectors.append({
#             'id': entry_id,
#             'values': chunk_embedding,
#             'metadata': {**metadata, 'chunk_index': chunk_idx}
#         })

# # Insert into Pinecone
# index.upsert(
#     vectors=vectors,
#     namespace="cma-app_pdf"
# )

# print("DEVELOPER NOTE: PDFs Uploaded")

## Upsert Websites to Pinecone DB
# csv_file = 'repository/Web_Links.csv'
# df = pd.read_csv(csv_file)
# print("DEVELOPER NOTE: Website CSV Loaded")

# chunk_size = 300
# chunk_overlap = 75
# vectors = []

# for idx, row in df.iterrows():
#     web_link = row['Web_Link']
#     print("The web link is:", web_link)

#     metadata = {
#         'main_topic': row['Main_Topic'],
#         'sub_topic': row['Sub_Topic'],
#         'sub_topic_question': row['Sub_Topic_Question'],
#         'web_link': web_link
#     }
    
#     # Load web content using WebBaseLoader
#     loader = WebBaseLoader(web_link)
#     documents = loader.load()
#     print("DEVELOPER NOTE: WebBaseLoader Successful")

#     # Split the content into chunks
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#     chunks = text_splitter.split_documents(documents)
#     print("DEVELOPER NOTE: Chunk Split is Successful")
#     print('this is chunks:', chunks)

#     for chunk_idx, chunk in enumerate(chunks):
#       print("DEVELOPER NOTE: Entering Chunk Embedding")
#       chunk_text = chunk['page_content']
      
#       # Embed the chunk content
#       chunk_embedding = embeddings_model.embed_documents([chunk_text])[0]

#       # Use a unique ID for each chunk
#       entry_id = f"website-{idx}-chunk-{chunk_idx}"
#       print("DEVELOPER NOTE: Entry ID is:", entry_id)
#       print("DEVELOPER NOTE: Values is:", chunk_embedding)
#       print("DEVELOPER NOTE: Chunk Idx is:", chunk_idx)


#       # Append to vectors list
#       vectors.append({
#           'id': entry_id,
#           'values': chunk_embedding,
#           'metadata': {**metadata, 'chunk_index': chunk_idx}
#       })

# # Step 5: Insert into Pinecone
# index.upsert(
#     vectors=vectors,
#     namespace="cma-app_website"
# )

# print("DEVELOPER NOTE: Websites Uploaded")

# handler = StdOutCallbackHandler()

# Translation

def translate_to_tagalog(text):
    # Create the messages list
    messages = [
        SystemMessage(content="You are a helpful assistant that translates text to Tagalog. Omit 'Narito ang pagsasalin sa Tagalog ng text:'' from your response."),
        HumanMessage(content=f"Translate the following text to Tagalog with a friendly tone: {text}")
    ]
    
    # Generate the translation
    response = openai_llm(messages)
    return response.content
  

# Prompt Template
prompt_template_case_manager = """
Isa kang case manager assistant na may access sa database ng dokumento. Isang Overseas Filipino Worker mula sa Saudi Arabia ang nagtanong ng sumusunod:
---
Tanong: {query}
Pangunahing Paksa: {main_topic}
Paksa: {sub_topic}
---
Batay sa impormasyong ito, bumuo ng isang query upang makuha ang mga pinaka-kaugnay na dokumento mula sa database at siguraduhing ang iyong tugon ay nasa Tagalog at may palakaibigang tono.
"""

# Create a PromptTemplate instance
prompt = PromptTemplate(
    template=prompt_template_case_manager,
    input_variables=["query", "main_topic", "sub_topic"]
)

document_contents = "page_content"
metadata_field_info = [
    {"name": "main_topic", "type": "string"},
    {"name": "sub_topic", "type": "string"}]

def create_self_query_retriever(query, main_topic, sub_topic, llm = openai_llm, retriever = Pinecone(index), prompt_template = prompt_template_case_manager):
    # Fill the prompt template with the query and metadata
    filled_prompt = prompt_template.format(
       query=query,
       main_topic=main_topic,
       sub_topic=sub_topic)
    
    print(filled_prompt)  # Print the filled prompt for debugging
    # Create the SelfQueryRetriever using the filled prompt
    self_query_retriever = SelfQueryRetriever.from_llm(
        llm=llm,
        retriever=retriever,
        vectorstore=vectorstore,
        document_contents=document_contents,
        metadata_field_info=metadata_field_info)
    return self_query_retriever

def chatbot_(query, main_topic, sub_topic):
  self_query_retriever = create_self_query_retriever(query=query, main_topic=main_topic, sub_topic=sub_topic, llm = openai_llm, retriever = Pinecone(index), prompt_template = prompt_template_case_manager)
  print("DEVELOPER NOTE: SelQueryRetriever Initialized")

  memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
  conversational_chain = ConversationalRetrievalChain.from_llm(openai_llm, retriever= self_query_retriever, memory= memory)
  chat_history = memory.load_memory_variables({}).get("chat_history", [])
  result = conversational_chain(
        inputs={"question": query, "chat_history": chat_history}
    )
  response = result['answer']

  return translate_to_tagalog(response)

# csv_file_path = 'chat_history.csv'

# if not os.path.exists(csv_file_path):
#    with open(csv_file_path, 'w') as f:
#      f.write('Main_Topic, Sub_Topic, question,response\n')

# def append_to_csv(question, response, metadata):
#     metadata_values = ",".join(f'"{value}"' for value in metadata.values())
#     with open(csv_file_path, 'a') as f:
#         f.write(f'{metadata_values}, "{question}","{response}"\n')

# print("DEVELOPER NOTE: CSV append code")

# def retrieve_response(query):
#   print("Retrieval Started...")
#   qa = RetrievalQA.from_chain_type(
#     llm=openai_llm,  
#     chain_type="stuff",  
#     retriever=retriever
#     # chain_type_kwargs={"prompt": prompt}
#     )  
#   print("Retrieval Complete.")
#   return qa.run(query)
  
# def retrieve_response_with_sources(question):
#   qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(
#     llm = openai_llm,
#     retriever = retriever,
#     return_source_documents = True,
#     callbacks = [handler],
#     # chain_type_kwargs={"prompt": prompt}
#     )
#   return qa_with_sources({"question": question})

# print("DEVELOPER NOTE: Retrieval Response Complete")